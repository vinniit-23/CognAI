# backend/app/utils/descope.py
"""
Helpers to call Descope Outbound APIs.
NOTE: This demo uses Management API for token retrieval, so keep MANAGEMENT KEY server-side.
"""

import os
import requests
from typing import Optional, Dict

DESCOPE_PROJECT_ID = os.getenv("DESCOPE_PROJECT_ID")
DESCOPE_MANAGEMENT_KEY = os.getenv("DESCOPE_MANAGEMENT_KEY")

if not DESCOPE_PROJECT_ID or not DESCOPE_MANAGEMENT_KEY:
    # We defer raising until function calls so unit tests / dry runs can inspect code.
    pass

BASE_URL_MGMT = "https://api.descope.com/v1/mgmt/outbound/app"  # management endpoints
BASE_URL_OUTBOUND = "https://api.descope.com/v1/outbound/oauth"  # connect endpoint (non-mgmt)

def _auth_header_with_management() -> Dict[str, str]:
    if not DESCOPE_PROJECT_ID or not DESCOPE_MANAGEMENT_KEY:
        raise RuntimeError("DESCOPE_PROJECT_ID and DESCOPE_MANAGEMENT_KEY are required in env")
    return {"Authorization": f"Bearer {DESCOPE_PROJECT_ID}:{DESCOPE_MANAGEMENT_KEY}" , "Content-Type": "application/json"}

def get_connect_url(outbound_app_id: str, redirect_url: str, scopes: Optional[list] = None, user_id: Optional[str] = None) -> Dict:
    """
    Initiate outbound connect. Returns JSON containing 'url' to redirect the user.
    This calls the outbound oauth connect endpoint (server-side).
    """
    # Try using the public outbound oauth connect endpoint with management auth.
    url = f"{BASE_URL_OUTBOUND}/connect"
    payload = {
        "appId": outbound_app_id,
        "options": {
            "redirectUrl": redirect_url,
            "scopes": scopes or []
        }
    }
    if user_id:
        payload["userId"] = user_id  # optional
    headers = _auth_header_with_management()
    r = requests.post(url, headers=headers, json=payload, timeout=15)
    r.raise_for_status()
    return r.json()

def fetch_outbound_token_management(app_id: str, user_id: str, scopes: Optional[list] = None, with_refresh_token: bool = False) -> Dict:
    """
    Use the Management API to fetch the latest token for a user & outbound app.
    Endpoint: POST /v1/mgmt/outbound/app/user/token
    """
    url = f"{BASE_URL_MGMT}/user/token"
    payload = {
        "appId": app_id,
        "userId": user_id,
        "scopes": scopes or [],
        "options": {"withRefreshToken": with_refresh_token, "forceRefresh": False},
    }
    headers = _auth_header_with_management()
    r = requests.post(url, headers=headers, json=payload, timeout=15)
    r.raise_for_status()
    return r.json()
