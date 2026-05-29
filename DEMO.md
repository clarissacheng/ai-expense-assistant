# Demo Instructions

## Live Demo URLs

### Frontend (Vercel)

https://ai-expense-assistant-sepia.vercel.app/

### Backend API (Render)

https://ai-expense-assistant-cc.onrender.com

This project is deployed publicly and can be demonstrated directly through the hosted frontend application.

---

# Live Demo Workflow

## 1. Register and Login

1. Open the deployed frontend URL
2. Create a new account using the Register button
3. Login using the created credentials
4. Verify that the authenticated dashboard loads successfully

Expected behavior:

* Session cookie is created
* User-specific dashboard becomes accessible
* Unauthorized users cannot access receipt endpoints

---

## 2. Upload a Receipt

1. Select a receipt image file
2. Click "Upload Receipt"

Expected behavior:

* Receipt image is sent to the FastAPI backend
* OpenAI GPT-4.1 Vision extracts structured receipt data
* Store name, date, total, and items are displayed
* Estimated API cost is shown to the user

---

## 3. Edit Extracted Data

1. Modify extracted fields such as:

   * store name
   * item category
   * totals
   * date
   
2. Click "Save Corrections"

Expected behavior:

* Updated values persist in the database
* Corrected data appears in receipt history and analytics

---

## 4. View Spending Analytics

After saving receipts:

### Receipt History

* Displays saved receipts for the authenticated user

### Spending by Store

* Aggregates total spending per merchant

### Spending by Category

* Aggregates totals across categories

### Spending Dashboard

* Displays interactive spending charts using Recharts

Expected behavior:

* Data is isolated per user account
* Analytics update automatically after uploads

---

# Local Development Setup

## 1. Backend Setup

```bash
cd backend
python3 -m pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```text
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/cse291p
GLOBAL_DAILY_COST_CEILING=10.0
USER_MONTHLY_COST_CEILING=5.0
SESSION_COOKIE_SECURE=false
ALLOW_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## 2. Frontend Setup

```bash
cd frontend
npm install
```

Create a `.env` file inside `frontend/`:

```text
REACT_APP_API_BASE_URL=http://localhost:8000
```

---

## 3. Start Backend

```bash
cd backend
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

---

## 4. Start Frontend

In another terminal:

```bash
cd frontend
npm start
```

Open:
http://localhost:3000

---

# Production Deployment Notes

## Backend Deployment

Hosted on Render:
https://ai-expense-assistant-cc.onrender.com

Production backend configuration includes:

* FastAPI
* PostgreSQL support
* secure session cookies
* OpenAI API integration
* CORS configuration
* deployment environment variables

---

## Frontend Deployment

Hosted on Vercel:
https://ai-expense-assistant-sepia.vercel.app/

Production frontend configuration includes:

* React
* Axios API communication
* authenticated session handling
* analytics dashboard
* responsive card-based UI

---

# Architecture Summary

## Frontend

* React SPA
* Axios-based API communication
* Recharts analytics dashboard
* Authenticated session state

## Backend

* FastAPI REST API
* Session-cookie authentication
* Receipt extraction endpoints
* Spending analytics endpoints

## Database

* PostgreSQL-compatible persistence layer
* Per-user receipt isolation
* Persistent receipt history

## AI Pipeline

* OpenAI GPT-4.1 Vision receipt extraction
* Structured JSON receipt parsing
* Editable correction workflow

---

# Budget Guardrails

The application includes configurable AI spending protections:

* `GLOBAL_DAILY_COST_CEILING`
* `USER_MONTHLY_COST_CEILING`

Uploads are rejected if configured limits are exceeded.

---

# Recommended Demo Talking Points

* Secure cookie-based authentication instead of localStorage tokens
* Public deployment with separate frontend/backend hosting
* AI-powered multimodal receipt extraction
* Persistent analytics and receipt history
* Per-user data isolation
* Production-oriented deployment architecture
* Budget ceilings for OpenAI API cost protection

---

# Optional Database Migration

To migrate legacy SQLite data into PostgreSQL:

```bash
TARGET_DATABASE_URL="postgresql://user:pass@host:5432/cse291p" \
python3 backend/migrate_sqlite_to_postgres.py
```
