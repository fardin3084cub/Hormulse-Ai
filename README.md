# 🌿 Hormulse AI — Python Backend

**Full-stack AI wellness companion with free AI providers.**  
FastAPI · SQLAlchemy · Groq · Gemini · OpenRouter · HuggingFace

---

## Architecture

```
hormulse/
├── main.py                    ← FastAPI app entry point
├── requirements.txt
├── .env.example               ← Copy to .env and fill in
├── templates/
│   └── index.html             ← Full SPA frontend
├── static/                    ← CSS/JS assets (if any)
└── app/
    ├── config.py              ← Pydantic settings
    ├── database.py            ← Async SQLAlchemy
    ├── dependencies.py        ← JWT auth dependency
    ├── models/
    │   ├── user.py            ← User model
    │   ├── log.py             ← WellnessLog model
    │   ├── chat_message.py    ← ChatMessage model
    │   └── plan.py            ← DailyPlan model
    ├── routers/
    │   ├── auth.py            ← POST /api/auth/register|login
    │   ├── users.py           ← GET/PATCH /api/users/me
    │   ├── logs.py            ← CRUD /api/logs/ + analytics
    │   ├── chat.py            ← POST /api/chat/stream (SSE)
    │   ├── plans.py           ← GET /api/plans/today
    │   └── insights.py        ← GET /api/insights/{type}
    ├── services/
    │   ├── ai_service.py      ← Multi-provider AI (ALL 4 FREE APIs)
    │   └── auth_service.py    ← JWT + bcrypt
    └── middleware/
        └── rate_limit.py      ← 60 req/min rate limiter
```

---

## Quick Start

### 1. Clone & install

```bash
git clone https://github.com/your-username/hormulse-ai
cd hormulse-ai
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add at least ONE free API key
```

### 3. Get FREE API keys (takes 5 min)

| Provider | URL | Free tier |
|----------|-----|-----------|
| **Groq** (recommended) | https://console.groq.com | Unlimited, very fast |
| Google Gemini | https://aistudio.google.com | 1500 req/day |
| OpenRouter | https://openrouter.ai | Many free models |
| HuggingFace | https://huggingface.co/settings/tokens | Free inference |

Add them to your `.env`:
```env
GROQ_API_KEY=gsk_...
GOOGLE_GEMINI_API_KEY=AIza...
```

### 4. Run

```bash
python main.py
# → http://localhost:8000
```

The API auto-creates the SQLite database on first run.

---

## API Reference

### Auth
```
POST /api/auth/register   { email, password, name, goal, struggle }
POST /api/auth/login      { email, password }
→ { access_token, user }
```

### Logs
```
POST /api/logs/           { mood, energy, sleep_hours, stress, notes }
GET  /api/logs/           ?limit=30
GET  /api/logs/today
GET  /api/logs/streak
GET  /api/logs/analytics  ?days=30
```

### AI Chat (Streaming)
```
POST /api/chat/stream     { message }
→ Server-Sent Events (text/event-stream)
   data: <chunk>\n\n
   data: [DONE]\n\n

GET  /api/chat/history
DELETE /api/chat/history
```

### AI Insights
```
GET /api/insights/daily
GET /api/insights/sleep
GET /api/insights/energy
GET /api/insights/hormones
GET /api/insights/weekly
GET /api/insights/correlation
```

### Plans
```
GET /api/plans/today      ?force=false
GET /api/plans/history    ?limit=7
```

### Users
```
GET   /api/users/me
PATCH /api/users/me       { name, goal, struggle, preferred_provider, anthropic_api_key }
```

---

## AI Provider Fallback Chain

The app automatically tries providers in order:

```
Groq → Gemini → OpenRouter → HuggingFace → User's Anthropic key
```

If one fails (rate limit, network error, etc.), it silently moves to the next.  
You only need **one** API key for the app to work.

---

## Deploy to Production

### Railway / Render / Fly.io (easiest)

1. Push to GitHub
2. Connect repo to Railway/Render
3. Set environment variables in dashboard
4. Change `DATABASE_URL` to PostgreSQL

### Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8000
CMD ["python", "main.py"]
```

### Postgres for production

```env
DATABASE_URL=postgresql+asyncpg://user:pass@db-host/hormulse
```

Run migrations:
```bash
alembic init migrations
alembic revision --autogenerate -m "init"
alembic upgrade head
```

---

## Features

- ✅ **Real-time streaming AI chat** via Server-Sent Events
- ✅ **4 free AI providers** with automatic fallback
- ✅ **JWT authentication** (7-day tokens)
- ✅ **Wellness logging** (mood, energy, sleep, stress, water, exercise)
- ✅ **Streak tracking**
- ✅ **30/90-day analytics** with trend detection
- ✅ **AI-generated daily plans** (cached per day)
- ✅ **6 AI insight types** (sleep, energy, hormones, weekly, correlations)
- ✅ **Rate limiting** (60 req/min per IP)
- ✅ **Per-user AI provider preferences**
- ✅ **SQLite (dev) → PostgreSQL (prod)**

---

Built by Arman · Based on Hormulse AI (hormulseai.lovable.app)
