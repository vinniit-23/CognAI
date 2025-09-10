from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from app.utils.descope import get_connect_url_with_refresh
import requests
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest
import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # only for development

router = APIRouter()

REDIRECT_URI = "http://127.0.0.1:8000/auth/callback"

# Temporary in-memory token store
# ⚠️ In production, save these securely in a DB or secret manager
TOKEN_STORE = {}

# Define your Google OAuth client configuration here
client_config = {
    "web": {
        "client_id": "619294137221-mpkjfa0qr8ghtktfnoqjpr1gq7afopp3.apps.googleusercontent.com",
        "project_id": "YOUR_PROJECT_ID",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": [REDIRECT_URI]
    }
}

# Add both readonly + send scopes
flow = Flow.from_client_config(
    client_config,
    scopes=[
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.send",
        "openid",
        "email",
        "profile"
    ],
    redirect_uri=REDIRECT_URI
)

class ConnectRequest(BaseModel):
    refresh_token: str
    app_id: str = "gmail"
    redirect_url: str = "http://localhost:8080"
    scopes: list[str] = [
        "https://mail.google.com/"
    ]

# Step 1: Descope connect with refresh token
@router.post("/auth/connect")
def connect_gmail(req: ConnectRequest, request: Request):
    print("CALLBACK URL:", request.url) 
    try:
        connect_data = get_connect_url_with_refresh(
            refresh_token=req.refresh_token,
            app_id=req.app_id,
            redirect_url=req.redirect_url,
            scopes=req.scopes,
        )
        
        # Descope SDK may return 'url' or 'redirect_url', wrap it explicitly
        redirect_url = connect_data.get("redirect_url") or connect_data.get("url")
        if not redirect_url:
            raise HTTPException(
                status_code=500,
                detail="Descope did not return a redirect URL"
            )
        
        return {"redirect_url": redirect_url}

    except requests.HTTPError as e:
        if e.response.status_code == 401:
            raise HTTPException(
                status_code=401,
                detail="Refresh token expired or revoked. Please re-authenticate."
            )
        raise


# Step 2: OAuth login URL
@router.get("/auth/login")
def login():
    auth_url, state = flow.authorization_url(
        access_type="offline",   # ensures refresh token
        include_granted_scopes="true",
        prompt="consent"         # force refresh token every time
    )
    TOKEN_STORE["state"] = state
    return {"auth_url": auth_url}

@router.get("/auth/callback")
def callback(request: Request):
    from fastapi.responses import JSONResponse
    
    # Debug log incoming request
    print("CALLBACK URL:", request.url)
    
    if "code" not in str(request.url):
        return JSONResponse(
            status_code=400,
            content={"error": "Missing ?code in callback URL. Did you log in via /auth/login?"}
        )

    flow = Flow.from_client_config(
        client_config,
        scopes=[
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send",
            "openid", "email", "profile"
        ]
    )
    flow.redirect_uri = REDIRECT_URI

    try:
        flow.fetch_token(authorization_response=str(request.url))
    except Exception as e:
        print("ERROR fetching token:", e)
        raise HTTPException(status_code=500, detail=f"Token fetch failed: {str(e)}")

    creds: Credentials = flow.credentials
    TOKEN_STORE["access_token"] = creds.token
    TOKEN_STORE["refresh_token"] = creds.refresh_token
    TOKEN_STORE["id_token"] = creds.id_token

    return RedirectResponse(url="http://localhost:8080")



# Step 4: Utility endpoint to always get a fresh access token
@router.get("/auth/token")
def get_valid_token():
    if "refresh_token" not in TOKEN_STORE:
        raise HTTPException(status_code=401, detail="Not authenticated. Please login first.")

    creds = Credentials(
        token=TOKEN_STORE.get("access_token"),
        refresh_token=TOKEN_STORE.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_config["web"]["client_id"],
        client_secret=client_config["web"]["client_secret"],
        scopes=[
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send",
            "openid", "email", "profile"
        ]
    )

    # Refresh if expired
    if not creds.valid or creds.expired:
        try:
            creds.refresh(GoogleRequest())
            TOKEN_STORE["access_token"] = creds.token
        except Exception:
            raise HTTPException(status_code=401, detail="Refresh token invalid or revoked. Please login again.")

    return {"access_token": TOKEN_STORE["access_token"]}