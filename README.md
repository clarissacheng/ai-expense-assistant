# AI Expense Assistant

AI Expense Assistant is a deployed full-stack receipt scanning and spending analytics web application built with React, FastAPI, PostgreSQL-compatible persistence, and OpenAI Vision models.

The application allows authenticated users to upload receipt images, extract structured purchase information using multimodal AI, edit extracted receipt data, persist receipt history, and analyze spending trends through interactive dashboards.

This project extends the Assignment 2 document scanner into a production-oriented deployed system with:

* secure authentication
* live frontend/backend deployment
* AI-powered receipt extraction
* persistent analytics
* OpenAI budget guardrails
* production deployment infrastructure

---

# Live Deployment

## Frontend (Vercel)

https://ai-expense-assistant-sepia.vercel.app/

## Backend (Render)

https://ai-expense-assistant-cc.onrender.com

---

# Features

## Authentication

* user registration
* secure login/logout
* cookie-based session management
* per-user receipt isolation

## Receipt Extraction

* receipt image upload
* OpenAI GPT-4.1 Vision extraction
* structured JSON parsing
* editable extracted receipt fields

## Analytics

* receipt history
* spending by merchant
* spending by category
* interactive spending dashboard charts

## Cost Guardrails

* per-user monthly OpenAI cost ceilings
* global daily OpenAI cost ceilings
* upload rejection when limits are exceeded

## Deployment

* Vercel frontend hosting
* Render backend hosting
* PostgreSQL-compatible production architecture

---

# Technologies Used

## Frontend

* React
* Axios
* Recharts

## Backend

* FastAPI
* SQLAlchemy
* passlib
* uvicorn

## Database

* PostgreSQL
* SQLite fallback for local development

## AI / LLM

* OpenAI GPT-4.1 Vision API

## Deployment

* Vercel
* Render

---

# Repository Structure

```text id="3xn9ew"
.
├── backend/
│   ├── app.py
│   ├── db.py
│   ├── extractor.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   └── package.json
│
├── proposal/
│   ├── original-proposal.md
│   └── marked-proposal.md
│
├── transcripts/
├── README.md
├── DESIGN.md
└── DEMO.md
```

---

# Setup Instructions

# 1. Clone Repository

```bash id="z14g5j"
git clone <https://github.com/clarissacheng/ai-expense-assistant.git>
cd <ai-expense-assistante>
```

---

# 2. Backend Setup

```bash id="0h8x2v"
cd backend
python3 -m pip install -r requirements.txt
```

Create a `.env` file inside `backend/`.

Example:

## `.env.example`

```text id="2bdt44"
OPENAI_API_KEY=your_openai_api_key

DATABASE_URL=postgresql://postgres:password@localhost:5432/cse291p

GLOBAL_DAILY_COST_CEILING=10.0
USER_MONTHLY_COST_CEILING=5.0

SESSION_COOKIE_SECURE=false

ALLOW_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

# 3. Frontend Setup

```bash id="q03lcv"
cd ../frontend
npm install
```

Optional frontend `.env`:

```text id="3m62sv"
REACT_APP_API_BASE_URL=http://localhost:8000
```

---

# How to Run

## Start Backend

```bash id="l0f2w0"
cd backend
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

---

## Start Frontend

In another terminal:

```bash id="04b71m"
cd frontend
npm start
```

Open:
http://localhost:3000

---

# User Workflow

1. Register a new account
2. Login
3. Upload a receipt image
4. AI extracts structured receipt data
5. Edit extracted fields if needed
6. Save corrected receipt
7. View receipt history and analytics dashboards

---

# Pipeline Stages

## Stage 1 — Authentication

Users register and login using secure cookie-based sessions.

Why:

* supports multi-user deployment
* isolates user data
* enables persistent analytics

---

## Stage 2 — Receipt Upload

Frontend uploads receipt images to the FastAPI backend.

Why:

* separates frontend UI from backend processing
* allows centralized AI and database handling

---

## Stage 3 — AI Receipt Extraction

`backend/extractor.py` sends receipt images to OpenAI GPT-4.1 Vision and requests structured JSON output.

Why:

* multimodal models perform well on noisy receipt images
* structured JSON improves downstream reliability

---

## Stage 4 — Human Correction Workflow

Users review and edit extracted receipt fields before saving.

Why:

* AI extraction is imperfect
* user corrections improve data quality
* increases trust in analytics accuracy

---

## Stage 5 — Persistence Layer

Corrected receipts are stored in PostgreSQL-compatible persistence.

Why:

* enables persistent history
* supports analytics aggregation
* supports deployment scalability

---

## Stage 6 — Analytics Dashboard

The frontend displays:

* merchant totals
* category totals
* spending charts

Why:

* converts extracted receipts into actionable spending insights

---

# Deployment Guide

## Backend Deployment (Render)

Start command:

```bash id="rw8fxn"
uvicorn backend.app:app --host 0.0.0.0 --port $PORT
```

Required environment variables:

* `DATABASE_URL`
* `OPENAI_API_KEY`
* `SESSION_COOKIE_SECURE=true`
* `ALLOW_ORIGINS`
* `GLOBAL_DAILY_COST_CEILING`
* `USER_MONTHLY_COST_CEILING`

---

## Frontend Deployment (Vercel)

Required environment variable:

```text id="db0hwf"
REACT_APP_API_BASE_URL=https://ai-expense-assistant-cc.onrender.com
```

---

# Eval Results

This project focuses primarily on deployment, authentication, and production AI integration rather than benchmark classification metrics.

However, qualitative evaluation was performed across:

* receipt extraction correctness
* dashboard consistency
* authentication reliability
* deployment stability

| Component           | Evaluation Result                                                                         |
| ------------------- | ----------------------------------------------------------------------------------------- |
| Authentication flow | Stable after cookie/CORS deployment fixes                                                 |
| Receipt extraction  | Successfully extracts merchant, totals, dates, and items on common grocery/store receipts |
| Correction workflow | Users can reliably fix extraction mistakes                                                |
| Analytics           | Correctly aggregates spending totals                                                      |
| Deployment          | Public frontend/backend deployment functioning successfully                               |

---

# Cost Controls

The backend enforces:

* per-user monthly AI spending ceilings
* global daily AI spending ceilings

This prevents runaway OpenAI API usage costs.

Environment variables:

* `GLOBAL_DAILY_COST_CEILING`
* `USER_MONTHLY_COST_CEILING`

---

# AI Transcripts

AI interaction transcripts are included in:

```text id="2ub29v"
transcripts/
```

These transcripts document:

* debugging workflows
* deployment troubleshooting
* frontend UI iteration
* authentication fixes
* architecture discussions

---

# Demo Video

YouTube demo link:

```
[Demo Video](https://drive.google.com/file/d/1OmqLH296ERY-5ax_RIC-AQP1PT4eNteQ/view?usp=sharing)
```

The demo video includes:

* deployment walkthrough
* authentication flow
* receipt upload and extraction
* editing workflow
* analytics dashboard
* architecture discussion

---

# Design Documentation

Additional architecture and design decisions are documented in:

* `DESIGN.md`
* `DEMO.md`
* `proposal/marked-proposal.md`

---

# Notes

## Local SQLite Support

If `DATABASE_URL` is omitted, the backend automatically falls back to local SQLite storage.

This is intended only for local development.

Production deployment should use PostgreSQL-compatible persistence.

---

# Known Challenges During Development

The most difficult engineering challenges involved:

* CORS configuration
* cookie/session persistence
* frontend/backend deployment integration
* password hashing compatibility
* Render deployment debugging

rather than the OpenAI extraction pipeline itself.

---

# Future Improvements

Planned future enhancements:

* natural-language budgeting insights
* recurring purchase detection
* multi-month trend analytics
* smarter category prediction
* receipt search and filtering
