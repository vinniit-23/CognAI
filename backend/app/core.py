"""
LLM wrapper: simple Gemini (google.generativeai) helper.
Keep this small so you can later wire LangChain on top of it.
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY in .env")

genai.configure(api_key=GOOGLE_API_KEY)

def llm_generate(prompt: str, model_name: str = "gemini-1.5-flash", max_output_tokens: int = 512) -> str:
    model = genai.GenerativeModel(model_name)
    
    # ✅ Use GenerationConfig to set parameters properly
    generation_config = genai.types.GenerationConfig(
        max_output_tokens=max_output_tokens,  # ✅ This is the correct parameter name
        temperature=0.7,  # Optional: adjust creativity
        top_p=0.95,       # Optional: nucleus sampling
        top_k=40          # Optional: top-k sampling
    )
    
    try:
        resp = model.generate_content(
            prompt, 
            generation_config=generation_config  # ✅ Pass config object
        )
        # ✅ Better text extraction with fallbacks
        if hasattr(resp, 'text') and resp.text:
            return resp.text
        elif resp.candidates and len(resp.candidates) > 0:
            candidate = resp.candidates[0]
            if candidate.content and candidate.content.parts:
                return candidate.content.parts[0].text
        return ""
    except Exception as e:
        # ✅ Better error handling
        print(f"LLM Generation Error: {str(e)}")
        raise Exception(f"Failed to generate content: {str(e)}")
