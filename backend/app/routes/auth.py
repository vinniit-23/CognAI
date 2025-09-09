# backend/app/routes/auth.py
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Optional
from ..utils import descope as descope_utils
import os
import traceback
import requests

router = APIRouter()
TOKEN_STORE: Dict[str, dict] = {}  # Persist to DB in prod


class ConnectRequest(BaseModel):
    user_id: Optional[str] = None
    redirect_url: str = "http://localhost:8080"
    session_token: Optional[str] = None


@router.post("/connect", response_model=dict)
def connect(req: ConnectRequest, authorization: Optional[str] = Header(None)):
    """
    Connect endpoint:
    - Accepts Descope session token in body or Authorization header.
    - Validates session server-side (if possible).
    - Calls Descope outbound /connect with management key.
    """

    # --- Extract session token ---
    session_token = req.session_token
    if not session_token and authorization:
        if authorization.lower().startswith("bearer "):
            session_token = authorization.split(" ", 1)[1].strip()

    if not req.user_id or not session_token:
        raise HTTPException(
            status_code=400,
            detail="user_id and session_token are required. Provide session_token in body or Authorization header."
        )

    # --- Validate session token (server-side) ---
    try:
        validated_session = descope_utils.validate_session_token(session_token)
        descope_user_id = (
            validated_session.get("userId")
            or validated_session.get("sub")
            or (validated_session.get("user") and validated_session["user"].get("userId"))
            or (validated_session.get("user") and validated_session["user"].get("id"))
        )
        if descope_user_id and descope_user_id != req.user_id:
            raise HTTPException(status_code=401, detail="Session token does not match provided user_id")

    except HTTPException:
        raise
    except Exception as e:
        print("[auth.connect] Session validation failed:", str(e))
        traceback.print_exc()
        # Fallback: allow outbound connect to proceed (dev mode)
        validated_session = None

    # --- Outbound connect to Descope ---
    try:
        result = descope_utils.get_connect_url(
            outbound_app_id=os.getenv("OUTBOUND_APP_ID", "gmail"),
            redirect_url=req.redirect_url,
            scopes=[
                "https://www.googleapis.com/auth/gmail.readonly",
                "https://www.googleapis.com/auth/gmail.send",
            ],
            user_id=req.user_id,
            session_token=session_token,
        )
        return result

    except requests.HTTPError as http_err:
        print("Descope outbound failed (HTTPError):", str(http_err))
        traceback.print_exc()
        raise HTTPException(status_code=502, detail="Descope outbound connect failed")

    except Exception as e:
        print("Descope outbound failed:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Descope outbound connect failed")
