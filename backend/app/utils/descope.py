# backend/app/utils/descope.py
"""
Descope helpers for backend.
- Uses the official Descope Python SDK for session validation.
- Uses REST for outbound connect (but supplies the correct auth-management key).
"""

import os
import requests
from typing import Optional, Dict, Any

# Try to use the SDK where appropriate (session validation, mgmt operations)
try:
    from descope import DescopeClient
except Exception:
    DescopeClient = None  # we'll handle absence gracefully

# Environment variables
DESCOPE_PROJECT_ID = os.getenv("DESCOPE_PROJECT_ID")
DESCOPE_MANAGEMENT_KEY = os.getenv("DESCOPE_MANAGEMENT_KEY")
DESCOPE_AUTH_MANAGEMENT_KEY = os.getenv("DESCOPE_AUTH_MANAGEMENT_KEY") or DESCOPE_MANAGEMENT_KEY
DESCOPE_BASE_URL = os.getenv("DESCOPE_BASE_URL", "https://api.descope.com")

# Base URLs
BASE_URL_MGMT = f"{DESCOPE_BASE_URL}/v1/mgmt/outbound/app"
BASE_URL_OUTBOUND = f"{DESCOPE_BASE_URL}/v1/outbound/oauth"
BASE_URL_SESSIONS = f"{DESCOPE_BASE_URL}/v1/sessions"

# SDK client singleton
_descope_client = None


def get_descope_client() -> Optional[Any]:
    """
    Initialize and return DescopeClient instance (cached).
    Requires DESCOPE_PROJECT_ID and either DESCOPE_MANAGEMENT_KEY or DESCOPE_AUTH_MANAGEMENT_KEY.
    """
    global _descope_client
    if _descope_client is not None:
        return _descope_client

    if DescopeClient is None:
        # SDK not installed
        return None

    if not DESCOPE_PROJECT_ID:
        raise RuntimeError("DESCOPE_PROJECT_ID env var is required to initialize DescopeClient")

    # prefer explicit management_key / auth_management_key when available
    kwargs = {"project_id": DESCOPE_PROJECT_ID}
    if DESCOPE_MANAGEMENT_KEY:
        kwargs["management_key"] = DESCOPE_MANAGEMENT_KEY
    if DESCOPE_AUTH_MANAGEMENT_KEY:
        # SDK optionally supports auth_management_key; supply it if available
        kwargs["auth_management_key"] = DESCOPE_AUTH_MANAGEMENT_KEY

    _descope_client = DescopeClient(**kwargs)
    return _descope_client


def _bearer_for(project_id: str, key: str) -> str:
    return f"Bearer {project_id}:{key}"


def _auth_header_for_auth_endpoints() -> Dict[str, str]:
    """
    Use auth-management key for auth-related endpoints (session validation, outbound connect).
    Falls back to DESCOPE_MANAGEMENT_KEY if DESCOPE_AUTH_MANAGEMENT_KEY not set.
    """
    if not DESCOPE_PROJECT_ID or not DESCOPE_AUTH_MANAGEMENT_KEY:
        raise RuntimeError("DESCOPE_PROJECT_ID and DESCOPE_AUTH_MANAGEMENT_KEY must be set for auth operations")
    return {
        "Authorization": _bearer_for(DESCOPE_PROJECT_ID, DESCOPE_AUTH_MANAGEMENT_KEY),
        "Content-Type": "application/json",
    }


def _auth_header_for_mgmt() -> Dict[str, str]:
    """
    Use the management key for management API calls.
    """
    if not DESCOPE_PROJECT_ID or not DESCOPE_MANAGEMENT_KEY:
        raise RuntimeError("DESCOPE_PROJECT_ID and DESCOPE_MANAGEMENT_KEY must be set for management operations")
    return {
        "Authorization": _bearer_for(DESCOPE_PROJECT_ID, DESCOPE_MANAGEMENT_KEY),
        "Content-Type": "application/json",
    }


def get_connect_url(
    outbound_app_id: str,
    redirect_url: str = "http://localhost:5173",
    scopes: Optional[list] = None,
    user_id: Optional[str] = None,
    session_token: Optional[str] = None,
) -> Dict[str, str]:
    """
    Build a redirect URL for an outbound app (Google/Gmail).
    Returns: {"redirect_url": "<url>"}
    Notes:
      - Descope docs: POST /v1/outbound/oauth/connect with Authorization: Bearer <PROJECT>:<AUTH_KEY>
      - We call it with the auth-management key to ensure it works even if auth public APIs are disabled.
    """
    url = f"{BASE_URL_OUTBOUND}/connect"
    payload: Dict[str, Any] = {
        "appId": outbound_app_id,
        "redirectURL": redirect_url,
        "scopes": scopes or [],
    }
    if user_id:
        payload["userId"] = user_id
    if session_token:
        payload["session"] = session_token

    headers = _auth_header_for_auth_endpoints()
    r = requests.post(url, headers=headers, json=payload, timeout=15)
    r.raise_for_status()
    data = r.json()
    # docs return `url` field in JSON
    return {"redirect_url": data.get("url")}


def fetch_outbound_token_management(
    app_id: str,
    user_id: str,
    scopes: Optional[list] = None,
    with_refresh_token: bool = False,
) -> Dict:
    """
    Management API: fetch token for user/outbound app via mgmt endpoint.
    Uses the management key.
    """
    if not user_id:
        raise ValueError("user_id is required")
    url = f"{BASE_URL_MGMT}/user/token"
    payload = {
        "appId": app_id,
        "userId": user_id,
        "scopes": scopes or [],
        "options": {"withRefreshToken": with_refresh_token, "forceRefresh": False},
    }
    headers = _auth_header_for_mgmt()
    r = requests.post(url, headers=headers, json=payload, timeout=15)
    r.raise_for_status()
    return r.json()


def validate_session_token(session_token: str) -> Dict:
    """
    Validate a Descope session token server-side.

    Preferred: use the Descope Python SDK validate_session which does the correct checks.
    Fallback: call REST validate endpoint (requires DESCOPE_AUTH_MANAGEMENT_KEY).
    """
    if not session_token:
        raise ValueError("session_token required")

    # Try SDK first (recommended)
    client = get_descope_client()
    if client is not None:
        try:
            # SDK exposes validate_session / validate_and_refresh_session methods.
            # This will raise on invalid/expired sessions.
            jwt_response = client.validate_session(session_token)
            # return jwt-like response (claims etc). Keep shape consistent.
            return jwt_response
        except Exception as e:
            # bubble up a clear error for debugging
            raise RuntimeError(f"Descope SDK session validation failed: {str(e)}")

    # Fallback to REST validate endpoint if SDK not installed
    url = f"{BASE_URL_SESSIONS}/validate"
    headers = _auth_header_for_auth_endpoints()
    payload = {"session": session_token}
    r = requests.post(url, headers=headers, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()
