# Demo Instructions

This document describes how to run the app locally and demonstrate its core functionality. It also includes the exact workflows to show during a demo and the deployment readiness checks for submission.

## Local demo setup

### 1. Backend setup
```bash
cd backend
python3 -m pip install -r requirements.txt
```
Create a `.env` file in `backend/` with:
```text
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/cse291p
GLOBAL_DAILY_COST_CEILING=10.0
USER_MONTHLY_COST_CEILING=5.0
SESSION_COOKIE_SECURE=false
ALLOW_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 2. Frontend setup
```bash
cd ../frontend
npm install
```

### 3. Start services
```bash
cd ../backend
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```
In another terminal:
```bash
cd frontend
npm start
```
Open the app at `http://localhost:3000`.

## Demo flow

### 1. Register and login
- Open the login screen
- Create a new account
- Confirm the session is established and the dashboard loads

### 2. Upload a receipt
- Choose a receipt image file
- Submit the upload
- Confirm the app displays extracted store name, date, total, and items
- Verify the estimated API cost message appears

### 3. Correct receipt data
- Change a store name, date, total, or item category
- Save the corrected receipt
- Confirm the backend persists the changes

### 4. View spending analytics
- Open the receipt history section
- Verify merchant spending totals are shown
- Verify category spending summary is shown
- Confirm the spending dashboard chart renders correctly

### 5. Budget guardrail verification
- Explain that uploads are blocked if monthly or global AI spending exceeds configured limits
- Optionally demonstrate by lowering `GLOBAL_DAILY_COST_CEILING` and triggering a budget rejection

## Production demo notes

### Backend deployment requirements
- Render or Railway backend deployment
- Managed Postgres instance with `DATABASE_URL`
- `OPENAI_API_KEY` configured in environment
- `SESSION_COOKIE_SECURE=true` in production

### Frontend deployment requirements
- Vercel or Netlify frontend deployment
- `REACT_APP_API_BASE_URL` pointing to the deployed backend

### Expected deployment behavior
- Backend should start cleanly and connect to Postgres
- Frontend should load and authenticate against the live backend
- Receipt uploads and analytics should work from the deployed URL

## Notes for submission
- This demo covers the full end-to-end stack from frontend to backend to database
- The app is intentionally built for hosted production with Postgres compatibility
- The records shown in analytics are generated from persisted receipts and reflect user-specific history

## Optional migration instructions
If you have legacy SQLite data to migrate to the hosted database:
```bash
TARGET_DATABASE_URL="postgresql://user:pass@host:5432/cse291p" \
  python3 backend/migrate_sqlite_to_postgres.py
```

## Recommended talking points
- Secure cookie-based auth avoids storing tokens in localStorage
- Postgres support is production-ready and required for deployment
- AI extraction is constrained to structured JSON for reliability
- Budget ceilings protect against unexpected OpenAI spend
