# AI Expense Assistant

A polished receipt scanner and spending analytics web app built with React, FastAPI, and PostgreSQL. The project supports secure authentication, AI-powered receipt parsing, user-correctable receipt data, persistent history, and budget-aware API usage.

## What this app does
- User registration and login using secure username/password authentication
- Cookie-based sessions with `httpOnly` support
- Receipt upload, AI extraction, and editable receipt fields
- Receipt history with persistent storage
- Spending summaries by merchant and category
- Budget controls for OpenAI API cost usage

## Project status
- **Frontend**: complete React UI with upload, edit, and analytics flows
- **Backend**: complete FastAPI backend with auth, receipt persistence, and guardrails
- **Database**: Postgres-ready schema with SQLAlchemy and optional local SQLite fallback
- **AI integration**: OpenAI Vision extraction with JSON enforcement and correction persistence

## Local setup
### 1. Backend
```bash
cd backend
python3 -m pip install -r requirements.txt
```
Create a `.env` file in `backend/` with at least:
```text
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/cse291p
GLOBAL_DAILY_COST_CEILING=10.0
USER_MONTHLY_COST_CEILING=5.0
SESSION_COOKIE_SECURE=false
ALLOW_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 2. Frontend
```bash
cd frontend
npm install
```
For local development the frontend can use CRA proxy and does not require `REACT_APP_API_BASE_URL`.

### 3. Run locally
```bash
cd backend
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```
In a separate window:
```bash
cd frontend
npm start
```
Open `http://localhost:3000`.

## Recommended database setup
This project is designed for Postgres in production. For local development, create a Postgres database and point `DATABASE_URL` at it.

Example:
```bash
createdb cse291p
```

If you want to use the fallback local SQLite store instead, omit `DATABASE_URL`; the backend will use `data/app.db` automatically. However, production deployment requires Postgres.

## Deployment guide
### Backend (Render)
1. Create a new Web Service and configure the root directory to `backend` if using the backend subfolder.
2. Set the build command:
   ```bash
   pip install -r requirements.txt
   ```
3. Set the start command:
   ```bash
   uvicorn backend.app:app --host 0.0.0.0 --port $PORT
   ```
4. Add required environment variables:
   - `DATABASE_URL`
   - `OPENAI_API_KEY`
   - `GLOBAL_DAILY_COST_CEILING=10.0`
   - `USER_MONTHLY_COST_CEILING=5.0`
   - `SESSION_COOKIE_SECURE=true`
   - `ALLOW_ORIGINS=https://your-frontend-url.com`
5. Deploy and verify the backend is healthy.

### Frontend (Vercel)
1. Create a Vercel project and connect the GitHub repo.
2. Set `REACT_APP_API_BASE_URL` to the deployed backend URL.
3. Deploy the frontend with default Create React App settings.

### Deployment troubleshooting
- If Render cannot reach Postgres, verify `DATABASE_URL` points to the hosted Postgres service, not `localhost`.
- If GitHub access is blocked, use a fork or personal repo as a temporary deployment branch.
- Keep backend secrets out of source control.

## Runtime configuration
### Backend uses
- `DATABASE_URL` — Postgres connection string
- `OPENAI_API_KEY` — OpenAI vision extraction key
- `SESSION_COOKIE_SECURE` — `true` in production
- `GLOBAL_DAILY_COST_CEILING` — default `10.0`
- `USER_MONTHLY_COST_CEILING` — default `5.0`
- `ALLOW_ORIGINS` — authorized frontend origins

### Frontend uses
- `REACT_APP_API_BASE_URL` — live backend URL for production

## User workflow
1. Register a new account
2. Login
3. Upload a receipt image
4. Review extracted receipt fields
5. Correct any items or totals
6. Save receipt data
7. View spending summaries and category analytics

## Submission deliverables
- `README.md` with installation, local development, and deployment instructions
- `DESIGN.md` describing architecture and data flow
- `DEMO.md` describing how to run and demo the app
- `PROJECT-PROPOSAL.md` describing project goals and technology
- source code for frontend and backend

## Notes for evaluators
This project has an end-to-end authenticated workflow, integrated AI receipt extraction, server-side budget guardrails, and a Postgres-ready deployment plan. The app is designed to transition from local development to hosted production with minimal configuration.
