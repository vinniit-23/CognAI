# backend/app/agents/fetcher.py
"""
Agent to fetch Gmail messages using token fetched/stored by the backend.
For demo, token_store is injected; in production use a secure DB.
"""

from typing import Dict, Any, List
from ..utils import gmail as gmail_utils

def fetch_messages_for_user(access_token: str, max_results: int = 10) -> Dict[str, Any]:
    """
    Returns list of parsed messages and metadata.
    """
    resp = gmail_utils.list_messages(access_token, max_results=max_results)
    messages = resp.get("messages", [])
    parsed = []
    for m in messages:
        try:
            msg_json = gmail_utils.get_message(access_token, m["id"])
            meta = gmail_utils.parse_message_meta(msg_json)
            parsed.append(meta)
        except Exception:
            # skip single failing message but continue
            continue
    return {
        "messages": parsed,
        "nextPageToken": resp.get("nextPageToken"),
        "resultSizeEstimate": resp.get("resultSizeEstimate", len(parsed))
    }
