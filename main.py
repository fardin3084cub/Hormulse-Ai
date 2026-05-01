"""
Hormulse AI — Production FastAPI Backend
Supports: Groq, Google Gemini, OpenRouter, HuggingFace (all free tiers)
"""

import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager

from app.routers import auth, logs, chat, plans, insights, users
from app.middleware.rate_limit import RateLimitMiddleware
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup & shutdown lifecycle."""
    await init_db()
    print("✅ Hormulse AI started. DB initialized.")
    yield
    print("🛑 Hormulse AI shutting down.")


app = FastAPI(
    title="Hormulse AI",
    description="AI-powered hormone & wellness companion — free APIs",
    version="2.0.0",
    lifespan=lifespan,
)

# ── CORS (allow any origin for dev; restrict in prod) ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Rate limiting ──
app.add_middleware(RateLimitMiddleware, max_requests=60, window_seconds=60)

# ── Static files & templates ──
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ── Routers ──
app.include_router(auth.router,     prefix="/api/auth",     tags=["auth"])
app.include_router(users.router,    prefix="/api/users",    tags=["users"])
app.include_router(logs.router,     prefix="/api/logs",     tags=["logs"])
app.include_router(chat.router,     prefix="/api/chat",     tags=["chat"])
app.include_router(plans.router,    prefix="/api/plans",    tags=["plans"])
app.include_router(insights.router, prefix="/api/insights", tags=["insights"])


@app.get("/", response_class=HTMLResponse)
async def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "2.0.0"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENV", "development") == "development",
        log_level="info",
    )
