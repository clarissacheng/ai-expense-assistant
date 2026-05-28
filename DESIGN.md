# Design Document

## Overview
AI Expense Assistant is a full-stack receipt scanning and spending analytics application. It is designed to provide authenticated users with secure receipt upload, structured AI extraction of receipt data, editable corrections, and persistent analytics backed by a production-ready database.

## Goals
- Provide secure user authentication
- Support AI-based receipt parsing with structured JSON output
- Enable user correction of extracted receipt data
- Persist receipts and analytics in a database
- Protect the app from runaway OpenAI costs with explicit budget limits

## System Architecture

### Frontend: React
The frontend handles:
- user registration and login
- receipt image upload
- display of extracted fields and items
- correction of receipt data
- saving corrected receipts
- presentation of receipt history and analytics

The app is configured to support local development through CRA proxy and production deployment through `REACT_APP_API_BASE_URL`.

### Backend: FastAPI
The backend handles:
- authentication endpoints (`/register/`, `/login/`, `/logout/`, `/me/`)
- receipt upload and extraction (`/upload/`)
- receipt correction persistence (`/receipt/{id}`)
- analytics endpoints (`/summary/`, `/category_summary/`, `/receipts/`, `/costs/`)
- correction mapping persistence (`/correct/`)

It also initializes the database schema on startup and applies legacy schema migration logic for SQLite-to-Postgres compatibility.

### Database Layer
The data model includes:
- `users`: accounts with hashed passwords
- `sessions`: secure session tokens and expiry times
- `receipts`: uploaded and corrected receipts with cost metadata

The backend supports:
- Postgres via `DATABASE_URL` for production
- local SQLite fallback when no `DATABASE_URL` is provided

### AI Extraction Pipeline
`backend/extractor.py` is responsible for:
- reading receipt images
- invoking OpenAI Vision
- enforcing structured JSON output
- normalizing merchant names and categories using correction mappings

## Data Model

### User
- `id`
- `username`
- `password_hash`

### Session
- `id`
- `user_id`
- `token`
- `expires_at`

### Receipt
- `id`
- `store_name`
- `date`
- `total`
- `raw_json`
- `user_id`
- `estimated_cost`
- `created_at`
- `draft`

## Request Flow
1. User logs in with credentials
2. Frontend sends authenticated requests with cookies
3. User uploads a receipt image to `/upload/`
4. Backend checks budget limits and calls OpenAI if allowed
5. Extracted receipt data is returned to the frontend
6. User edits receipt details and saves via `/receipt/{id}`
7. Backend stores the final receipt and updates analytics

## Budget Guardrails
The backend enforces two cost limits:
- **Per-user monthly limit**: default $5.00
- **Global daily limit**: default $10.00

If a new upload would exceed either limit, the backend rejects it before the AI call.

## Deployment Design
### Production target
- Backend: Render or Railway
- Frontend: Vercel or equivalent static host
- Database: managed Postgres via `DATABASE_URL`

### Runtime environment
Required environment variables:
- `DATABASE_URL`
- `OPENAI_API_KEY`
- `SESSION_COOKIE_SECURE`
- `GLOBAL_DAILY_COST_CEILING`
- `USER_MONTHLY_COST_CEILING`
- `ALLOW_ORIGINS`
- `REACT_APP_API_BASE_URL` (frontend)

### Backend startup
- install dependencies from `backend/requirements.txt`
- start with `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`

### Deployment considerations
- If GitHub integration is blocked, a fork or mirror repo can be used for Render/Vercel deployment
- Environment variables must be configured in the hosting service; secrets should never be committed
- `SESSION_COOKIE_SECURE=true` should be set in production with HTTPS enabled

## First Deliverable Workflow
1. User registers and logs in
2. Upload receipt image
3. Backend validates budget and extracts structured data
4. User reviews and corrects the receipt
5. User saves the corrected receipt
6. Analytics update with merchant and category spending

## Current Status
- Authentication is implemented
- receipt extraction and correction flows are implemented
- receipt history and analytics are implemented
- Postgres deployment path is documented
- production deployment is blocked only by GitHub integration approval

## Future Enhancements
- natural language spend summaries
- recurring purchase detection
- multi-month trend charts
- advanced category prediction
- receipt search and filtering
