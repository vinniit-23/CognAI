# backend/main.py
import os, requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# CORS so Streamlit (8501) can call FastAPI (8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DESCOPE_PROJECT_ID = os.getenv("DESCOPE_PROJECT_ID")
DESCOPE_MANAGEMENT_KEY = os.getenv("DESCOPE_MANAGEMENT_KEY")
DESCOPE_BASE = "https://api.descope.com"

class ConnectBody(BaseModel):
    user_id: str         # Descope userId (sub)
    refresh_jwt: str     # From login flow JSON

@app.post("/auth/connect")
def start_outbound_connect(body: ConnectBody):
    """
    1) Start Descope Outbound OAuth connect (uses refresh JWT).
    2) Returns a redirect URL - send user there to approve Gmail scopes.
    """
    url = f"{DESCOPE_BASE}/v1/outbound/oauth/connect"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DESCOPE_PROJECT_ID}:{body.refresh_jwt}",
    }
    payload = {
        "appId": "gmail",
        "options": {
            "redirectUrl": "http://localhost:8501"
            # omit "scopes" to use default app scopes configured in Console
        }
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    if r.status_code != 200:
        raise HTTPException(status_code=400, detail=r.json())
    return r.json()  # contains "redirectURL"

@app.get("/auth/token")
def get_outbound_token(user_id: str):
    """
    After user connected, fetch latest Gmail access token from Descope vault (Management API).
    """
    url = f"{DESCOPE_BASE}/v1/mgmt/outbound/app/user/token/latest"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DESCOPE_PROJECT_ID}:{DESCOPE_MANAGEMENT_KEY}",
    }
    payload = {
        "appId": "gmail",
        "userId": user_id,
        "options": {"withRefreshToken": False, "forceRefresh": False},
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    if r.status_code != 200:
        raise HTTPException(status_code=400, detail=r.text)
    return r.json()  # { token: { accessToken, ... }, ... }

@app.get("/emails")
def list_emails(user_id: str, max_results: int = 10):
    """
    Convenience endpoint:
    1) Pull token from Descope
    2) Call Gmail list messages
    """
    token = get_outbound_token(user_id)
    access_token = token["token"]["accessToken"]

    g_headers = {"Authorization": f"Bearer {access_token}"}
    g_params = {"maxResults": max_results}  # add q / labelIds as needed
    g_url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"

    gr = requests.get(g_url, headers=g_headers, params=g_params, timeout=30)
    if gr.status_code != 200:
        raise HTTPException(status_code=gr.status_code, detail=gr.text)
    return gr.json()
