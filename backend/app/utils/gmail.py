# backend/app/utils/gmail.py
import requests
from typing import Dict, Optional

GMAIL_API_BASE = "https://gmail.googleapis.com/gmail/v1"

def list_messages(access_token: str, user_id: str = "me", max_results: int = 10, page_token: Optional[str] = None) -> Dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"maxResults": max_results}
    if page_token:
        params["pageToken"] = page_token
    url = f"{GMAIL_API_BASE}/users/{user_id}/messages"
    r = requests.get(url, headers=headers, params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def get_message(access_token: str, message_id: str, user_id: str = "me") -> Dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{GMAIL_API_BASE}/users/{user_id}/messages/{message_id}"
    r = requests.get(url, headers=headers, params={"format": "full"}, timeout=15)
    r.raise_for_status()
    return r.json()

def parse_message_meta(message_json: Dict) -> Dict:
    snippet = message_json.get("snippet", "")
    payload = message_json.get("payload", {})
    headers = payload.get("headers", [])
    def _get_header(name):
        for h in headers:
            if h.get("name", "").lower() == name.lower():
                return h.get("value")
    return {
        "id": message_json.get("id"),
        "threadId": message_json.get("threadId"),
        "snippet": snippet,
        "from": _get_header("From"),
        "to": _get_header("To"),
        "subject": _get_header("Subject"),
        "date": _get_header("Date"),
    }
