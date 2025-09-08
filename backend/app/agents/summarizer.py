# backend/app/agents/summarizer.py
"""
Create a summarizer that uses core.llm_generate.
This is intentionally simple — feed list of snippets into a prompt.
"""

from typing import List
from ..core import llm_generate

def summarize_messages(messages: List[dict], max_lines: int = 5) -> str:
    if not messages:
        return "No messages found to summarize."
    snippets = []
    for m in messages[:50]:  # limit
        subject = m.get("subject","(no subject)")
        frm = m.get("from","")
        snippet = m.get("snippet","")
        snippets.append(f"From: {frm}\nSubject: {subject}\nSnippet: {snippet}\n---")
    prompt = (
        "You are an assistant. Summarize the following email snippets into concise bullets. "
        f"Return up to {max_lines} short bullets.\n\n" + "\n".join(snippets)
    )
    return llm_generate(prompt)
