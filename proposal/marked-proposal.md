# Marked-up Proposal

## Original Proposal

### Planned Technologies
- React
- FastAPI
- SQLAlchemy
- PostgreSQL (Render)
- SQLite
- OpenAI GPT-4.1 Vision API
- passlib

### First Deliverable
- Account creation
- Login with secure cookies
- Receipt upload
- Edit extracted data
- Save receipt
- Spending summaries
- Deploy-ready architecture

### Rough Architecture for First Deliverable
- React frontend: `frontend/src/App.js`
- FastAPI backend: `backend/app.py`
- DB layer: `backend/db.py`
- OpenAI extraction: `backend/extractor.py`
- Cost guardrails: `GET /costs/` and budget checks in `upload`
- Auth sessions: cookie-based in `backend/app.py`

### After First Deliverable Goals
- Budgeting insights
- Recurring purchases
- Trend charts
- Smarter category suggestions
- Receipt search

## Marked-up Proposal

### Planned Technologies
- React ✅ implemented in `frontend/src/App.js`
- FastAPI ✅ implemented in `backend/app.py`
- SQLAlchemy ✅ implemented in `backend/db.py`
- PostgreSQL (Render) ✅ supported through `DATABASE_URL` and documented in `README.md`
- SQLite ✅ supported locally by default in `backend/db.py` and described for local development in `README.md`
- OpenAI GPT-4.1 Vision API ✅ implemented in `backend/extractor.py`
- passlib ✅ implemented in `backend/db.py`

### First Deliverable
- Account creation ✅ implemented at `backend/app.py` `POST /register/`
- Login with secure cookies ✅ implemented at `backend/app.py` `POST /login/`, `GET /me/`, and session cookie handling in the login/logout flow
- Receipt upload ✅ implemented at `backend/app.py` `POST /upload/` and the React upload flow in `frontend/src/App.js`
- Edit extracted data ✅ implemented in `frontend/src/App.js` with editable receipt fields and `backend/app.py` `PUT /receipt/{id}` to save corrections
- Save receipt ✅ implemented in `backend/app.py` `PUT /receipt/{id}` and persisted in `backend/db.py`
- Spending summaries ✅ implemented in `backend/app.py` `GET /summary/` and `GET /category_summary/`, and displayed in `frontend/src/App.js`
- Deploy-ready architecture ✅ documented in `README.md`, `DESIGN.md`, and `DEMO.md`; backend build/setup commands are Render-compatible

### Rough Architecture for First Deliverable
- React frontend: `frontend/src/App.js` ✅
- FastAPI backend: `backend/app.py` ✅
- DB layer: `backend/db.py` ✅
- OpenAI extraction: `backend/extractor.py` ✅
- Cost guardrails: implemented in `backend/app.py` `/upload/` and exposed via `GET /costs/` ✅
- Auth sessions: cookie-based in `backend/app.py` ✅

### After First Deliverable Goals
- Budgeting insights: planned. This will extend existing analytics endpoints and dashboard components to surface natural-language or contextual budget advice.
- Recurring purchases: planned. This will fit into the receipt history analytics layer and new backend endpoints for repeated merchant/item detection.
- Trend charts: partially implemented with the current spending dashboard. Monthly and multi-month trends are planned as a next iteration in the frontend UI and backend query logic.
- Smarter category suggestions: planned. The existing correction persistence architecture in `backend/extractor.py` already supports this extension.
- Receipt search: planned. This would add a search/query endpoint in `backend/db.py` and a search UI in `frontend/src/App.js`.

### Notes
- No items are marked as no longer planned.
- The proposal remains consistent with the current implementation and future roadmap.
