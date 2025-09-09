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
    try:
        user_prompt_lower = req.user_prompt.lower()
        if ("summarize" in user_prompt_lower or "summary" in user_prompt_lower) and req.user_id:
            token_info = TOKEN_STORE.get(req.user_id)
            if not token_info:
                return ChatResponse(ai_response="Please connect your Gmail first.")
            access_token = token_info.get("accessToken") or token_info.get("access_token")
            from ..agents.fetcher import fetch_messages_for_user

            emails = fetch_messages_for_user(access_token, max_results=10)
            messages = emails.get("messages", [])
            summary = summarize_messages(messages, max_lines=6)
            return ChatResponse(ai_response=summary)

        # Default: generate as usual
        result = llm_generate(req.user_prompt)
        return ChatResponse(ai_response=result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Chat processing error: {str(e)}")
