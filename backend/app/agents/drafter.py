from ..core import llm_generate

def draft_reply(subject: str, snippet: str, tone: str = "professional", max_tokens: int = 256) -> str:
    prompt = (
        f"Draft a {tone} email reply for this message.\n\n"
        f"Subject: {subject}\nSnippet: {snippet}\n\nReply:"
    )
    # ✅ Use the updated function signature
    return llm_generate(prompt, max_output_tokens=max_tokens)
