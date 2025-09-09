# backend/app/routes/google.py
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
import os, json, traceback

router = APIRouter()

# Path to Google OAuth credentials
CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "credentials.json")

SCOPES = [
    "https://mail.google.com/",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/google/callback")

# Temporary in-memory store (replace with DB in production)
TOKEN_STORE = {}


@router.get("/google/connect")
def google_connect(user_id: str):
    """
    Start OAuth flow. user_id is passed as state.
    """
    try:
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI,
        )
        auth_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes=True,
            prompt="consent",
            state=user_id,  # send userId so callback knows who
        )
        return {"url": auth_url}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Google OAuth init failed: {str(e)}")


@router.get("/google/callback")
async def google_callback(request: Request):
    """
    Handle redirect from Google. Exchange code for tokens.
    """
    try:
        state = request.query_params.get("state")
        code = request.query_params.get("code")

        if not state:
            raise HTTPException(status_code=400, detail="Missing state (user_id)")
        if not code:
            raise HTTPException(status_code=400, detail="Missing authorization code")

        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI,
        )
        flow.fetch_token(authorization_response=str(request.url))

        creds = flow.credentials
        TOKEN_STORE[state] = {
            "accessToken": creds.token,
            "refreshToken": creds.refresh_token,
            "tokenExpiry": creds.expiry.isoformat() if creds.expiry else None,
        }

        # ✅ Redirect back to frontend (you can also return JSON if you prefer)
        frontend_url = f"http://localhost:8080?connected=true"
        return RedirectResponse(frontend_url)

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to complete Google OAuth: {str(e)}")
