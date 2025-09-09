# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

from .routes import auth, chat, emails

app = FastAPI(title="CognAI Backend")

# backend/app/main.py (CORS snippet)
FRONTEND_ORIGINS = os.getenv("FRONTEND_ORIGIN", "http://localhost:8080")
# allow comma-separated origins like: http://localhost:8080,http://192.168.1.5:8080
allow_origins = [o.strip() for o in FRONTEND_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(emails.router, prefix="/emails", tags=["emails"])

@app.get("/")
def root():
    return {"ok": True, "message": "CognAI backend running"}
