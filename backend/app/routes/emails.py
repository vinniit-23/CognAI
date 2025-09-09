# backend/app/routes/emails.py
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..routes.auth import TOKEN_STORE
from ..agents.fetcher import fetch_messages_for_user

router = APIRouter()

@router.get("/")
def list_emails(user_id: str, max_results: Optional[int] = Query(10, ge=1, le=100)):
    token_info = TOKEN_STORE.get(user_id)
    if not token_info:
        raise HTTPException(status_code=404, detail="No token found for user; please connect first")
    access_token = (
        token_info.get("accessToken")
        or token_info.get("access_token")
        or token_info.get("accessTokenValue")
    )
    if not access_token:
        raise HTTPException(status_code=500, detail="Access token missing in stored token information")
    try:
        data = fetch_messages_for_user(access_token, max_results=max_results)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gmail fetch error: {str(e)}")
