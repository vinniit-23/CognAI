from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from .routes import auth, chat, emails
from .routes import google as google_routes


load_dotenv()

app = FastAPI(title="CognAI Backend")

FRONTEND_ORIGINS = os.getenv("FRONTEND_ORIGIN", "http://localhost:8080")
allow_origins = [o.strip() for o in FRONTEND_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(emails.router, prefix="/emails", tags=["emails"])
app.include_router(google_routes.router, prefix="/google", tags=["google"])

@app.get("/")
def root():
    return {"ok": True, "message": "CognAI backend running"}
