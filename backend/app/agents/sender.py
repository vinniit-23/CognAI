# backend/app/agents/sender.py
"""
Create/send email via Gmail. This uses gmail.send_message helper which expects raw RFC822 bytes.
We provide a helper to build a minimal message.
"""
from email.mime.text import MIMEText
from ..utils import gmail as gmail_utils

def create_rfc822_message(to_email: str, subject: str, body: str, from_email: str) -> bytes:
    msg = MIMEText(body, "plain", "utf-8")
    msg["To"] = to_email
    msg["From"] = from_email
    msg["Subject"] = subject
    return msg.as_bytes()

def send_email(access_token: str, to_email: str, subject: str, body: str, from_email: str = "me") -> dict:
    raw = create_rfc822_message(to_email, subject, body, from_email)
    return gmail_utils.send_message(access_token, raw)
