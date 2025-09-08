# backend/app/routes/chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..core import llm_generate
from ..routes.auth import TOKEN_STORE
from ..agents.summarizer import summarize_messages

router = APIRouter()

class ChatRequest(BaseModel):
    user_prompt: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    ai_response: str

@router.post("/", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Handle prompt -> agent. If prompt asks for emails summary and user_id present,
    demonstrate fetching messages + summarizing. Otherwise forward to LLM.
    """
    user_prompt = req.user_prompt.lower()
    try:
        # A simple intent heuristic: if user asked for 'summarize' and provided user_id,
        # fetch messages and call summarizer.
        if ("summarize" in user_prompt or "summary" in user_prompt) and req.user_id:
            token_info = TOKEN_STORE.get(req.user_id)
            if not token_info:
                return ChatResponse(ai_response="Please connect your Gmail first.")
            access_token = token_info.get("accessToken") or token_info.get("access_token")
            # re-use fetcher
            from ..agents.fetcher import fetch_messages_for_user
            emails = fetch_messages_for_user(access_token, max_results=10)
            messages = emails.get("messages", [])
            summary = summarize_messages(messages, max_lines=6)
            return ChatResponse(ai_response=summary)
        # default — call LLM directly
        result = llm_generate(req.user_prompt)
        return ChatResponse(ai_response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
