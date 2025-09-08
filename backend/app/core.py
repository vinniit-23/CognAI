# backend/app/core.py
"""
Initialize LLM client and expose helper functions.
This wraps google.generativeai (Gemini). You can later plug LangChain here.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY in .env")

genai.configure(api_key=GOOGLE_API_KEY)

# simple wrapper
def llm_generate(prompt: str, model_name: str = "gemini-1.5-flash", max_output_tokens: int = 512) -> str:
    """
    Generate text using Gemini.
    Keep this function small so LangChain agents can reuse it later.
    """
    model = genai.GenerativeModel(model_name)
    try:
        resp = model.generate_content(prompt, max_output_tokens=max_output_tokens)
        return getattr(resp, "text", "") or ""
    except Exception as e:
        # bubble up or log
        raise
