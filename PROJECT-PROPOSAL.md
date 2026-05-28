# AI Expense Assistant

### Project Proposal
A secure, deployable receipt scanner and spending analytics app built with React, FastAPI, and PostgreSQL. The system enforces budget-safe AI usage, supports authenticated users, and stores receipt history for analytics.

---

## One Sentence Description
A hosted receipt extraction and analytics tool using secure cookie-based auth, AI vision extraction, and Postgres persistence with explicit API cost guardrails.

---

## Problem Statement
Many receipt scanning solutions either sacrifice security, rely on local data storage, or expose users to uncontrolled AI costs. This project delivers a complete end-to-end system that is safe for users, deployable in production, and mindful of API spending.

## Past Project Reference
This project is built as an extension of the Assignment 2 Document Scanner.

Repository reference:
https://github.com/ucsd-cse-genai-programming-sp26/02-doc-scanner-cc

The base work provided receipt upload and extraction. This final project advances it by adding:
- secure login and session management
- hosted backend architecture
- Postgres-ready persistence
- spending and budget analytics
- deployment readiness for Render and Vercel

---

## Technology Stack

### Frontend
- React
- Axios
- Recharts

### Backend
- FastAPI
- SQLAlchemy
- Python 3.x
- Uvicorn

### Database
- PostgreSQL for deployment
- SQLite fallback for local development only

### AI / LLM
- OpenAI GPT-4.1 Vision API for receipt extraction

### Authentication
- username/password auth
- bcrypt password hashing
- httpOnly cookie sessions

### DevOps and Infrastructure
- Render for backend deployment
- Vercel for frontend deployment
- environment-based configuration via `DATABASE_URL` and `OPENAI_API_KEY`

---

## First Deliverable: Goals
Deliver a functioning public web app that allows a user to:
1. Register and log in securely
2. Upload a receipt image
3. View AI-extracted receipt data
4. Correct receipt fields and item categories
5. Save corrected receipts to a persistent store
6. Review spending summaries by merchant and category
7. Access the app from a public URL with managed Postgres storage

### Success criteria
- Authentication is secure and session-based
- Receipt extraction is powered by OpenAI Vision
- Budget guardrails prevent excessive API usage
- Spending analytics are generated from persisted receipts
- Application is deployable to Render and Vercel

---

## Architecture Overview

### React Frontend
The frontend provides:
- login/register forms
- receipt upload and file handling
- extracted data editing UI
- save/correct flows
- analytics dashboard with merchant totals and category summaries

### FastAPI Backend
The backend provides:
- auth endpoints (`/register/`, `/login/`, `/logout/`, `/me/`)
- upload endpoint (`/upload/`) with budget validation
- receipt save endpoint (`/receipt/{id}`)
- analytics endpoints (`/summary/`, `/category_summary/`, `/receipts/`)
- correction persistence endpoint (`/correct/`)

### Database Layer
The backend uses SQLAlchemy to model:
- `users`
- `sessions`
- `receipts`

It supports both local SQLite and production Postgres via `DATABASE_URL`.

### AI Pipeline
`backend/extractor.py` handles receipt image ingestion, calls OpenAI Vision, parses JSON, and normalizes results. Corrections are applied to merchant names and item categories.

### Budget Guardrails
The upload flow checks:
- per-user monthly estimated cost
- global daily estimated cost

Requests are rejected before calling OpenAI if limits are exceeded.

---

## Deployment Plan
### Backend deployment
Primary deployment target is Render. The backend is configured for hosted Postgres and environment-driven startup.

Required Render environment variables:
- `DATABASE_URL`
- `OPENAI_API_KEY`
- `SESSION_COOKIE_SECURE=true`
- `GLOBAL_DAILY_COST_CEILING=10.0`
- `USER_MONTHLY_COST_CEILING=5.0`
- `ALLOW_ORIGINS=https://your-frontend-url` (or local dev origin)

Recommended build/start commands:
```bash
pip install -r requirements.txt
uvicorn backend.app:app --host 0.0.0.0 --port $PORT
```

### Frontend deployment
Primary deployment target is Vercel.

Required Vercel environment variable:
- `REACT_APP_API_BASE_URL=https://your-backend.onrender.com`

### Deployment blockers and workarounds
- If GitHub organization permission blocks Render/Vercel, use a fork or personal repo copy to deploy.
- Do not commit any secret credentials or database URLs.

---

## Implementation Status
The current codebase implements:
- secure user auth and session cookies
- receipt upload, extraction, and correction workflows
- persistent receipt history and analytics
- budget controls for AI usage
- deployment documentation for Render/Vercel

Remaining work for finalization:
- connect Render/Vercel to the repo once org approvals arrive
- provision hosted Postgres and run the migration
- publish frontend with the live backend URL

---

## Future Enhancements
- natural-language spending summaries
- recurring expense detection
- multi-month trend analysis
- improved item categorization suggestions
- receipt search and filtering

