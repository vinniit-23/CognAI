# backend/app/routes/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from ..utils import descope as descope_utils
import os

router = APIRouter()

# In-memory token store for demo { user_id -> {access_token, expires_at, raw_response} }
TOKEN_STORE: Dict[str, dict] = {}

class ConnectRequest(BaseModel):
    user_id: str
    redirect_url: str = "http://localhost:5173"  # frontend origin by default

@router.post("/connect")
def connect(req: ConnectRequest):
    """
    Generate a connect URL for a given outbound app (gmail). Returns { url }.
    Frontend should redirect the user to this URL to begin the OAuth consent.
    """
    try:
        result = descope_utils.get_connect_url(outbound_app_id="gmail", redirect_url=req.redirect_url, scopes=[
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send"
        ], user_id=req.user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result  # expected to contain 'url'

class NotifyRequest(BaseModel):
    user_id: str

@router.post("/notify-connection")
def notify_connection(req: NotifyRequest):
    """
    After user connects and Descope completed OAuth, frontend informs backend with user_id.
    Backend uses Management API to fetch the token for that user and stores it temporarily.
    """
    try:
        data = descope_utils.fetch_outbound_token_management(app_id="gmail", user_id=req.user_id, scopes=[
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send"
        ])
        # Response contains a token object. Adapt to exact Descope shape.
        token_obj = data.get("token") or data
        # token_obj expected fields: accessToken, refreshToken, expiresIn, scope
        TOKEN_STORE[req.user_id] = token_obj
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch token: {e}")

@router.get("/tokens")
def debug_tokens():
    """
    Dev-only: return in-memory tokens. REMOVE in production.
    """
    return TOKEN_STORE
