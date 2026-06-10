# Marked-up Proposal

## Original Proposal

### Planned Technologies

* React
* FastAPI
* SQLAlchemy
* PostgreSQL (Render)
* SQLite
* OpenAI GPT-4.1 Vision API
* passlib

### First Deliverable

* Account creation
* Login with secure session cookies and per-user authentication isolation
* Receipt upload
* Edit extracted data
* Save receipt
* Spending summaries
* Deploy-ready architecture

### Rough Architecture for First Deliverable

* React frontend: `frontend/src/App.jsx`
* FastAPI backend: `backend/app.py`
* DB layer: `backend/db.py`
* OpenAI extraction: `backend/extractor.py`
* Cost guardrails: `GET /costs/` and budget checks in `upload`
* Auth sessions: cookie-based in `backend/app.py`

### After First Deliverable Goals

* Budgeting insights
* Recurring purchases
* Trend charts
* Smarter category suggestions
* Receipt search

---

## Marked-up Proposal

### Planned Technologies

* React ✅ implemented in `frontend/src/App.jsx`
* FastAPI ✅ implemented in `backend/app.py`
* SQLAlchemy ✅ implemented in `backend/db.py`
* PostgreSQL (Render) ✅ supported through `DATABASE_URL` and documented in `README.md`
* SQLite ✅ supported locally by default in `backend/db.py` and documented in `README.md`
* OpenAI GPT-4.1 Vision API ✅ implemented in `backend/extractor.py`
* passlib ✅ implemented in `backend/db.py`
* Vercel ✅ used for frontend deployment
* Render ✅ used for backend deployment

### First Deliverable

* Account creation ✅ implemented at `backend/app.py` with `POST /register/`
* Login with secure session cookies and per-user authentication isolation ✅ implemented at `backend/app.py` with `POST /login/`, `POST /logout/`, and `GET /me/`
* Password hashing ✅ implemented in `backend/db.py` using `passlib`
* Receipt upload ✅ implemented at `backend/app.py` `POST /upload/` and integrated into the React upload flow in `frontend/src/App.jsx`
* Edit extracted data ✅ implemented in `frontend/src/App.jsx` with editable receipt fields and `backend/app.py` `PUT /receipt/{id}`
* Save receipt ✅ implemented in `backend/db.py` and persisted through backend update endpoints
* Spending summaries ✅ implemented through `GET /summary/` and `GET /category_summary/` endpoints and displayed in the dashboard UI
* Deploy-ready architecture ✅ implemented and publicly deployed using Vercel (frontend) and Render (backend)
* Cost estimation guardrails ✅ implemented in the upload pipeline and surfaced to users after receipt extraction

### Rough Architecture for First Deliverable

* React frontend: `frontend/src/App.jsx` ✅ implemented
* FastAPI backend: `backend/app.py` ✅ implemented
* Database layer: `backend/db.py` ✅ implemented
* OpenAI extraction pipeline: `backend/extractor.py` ✅ implemented
* Cost guardrails: implemented in `backend/app.py` upload handling and exposed through API cost estimation logic ✅
* Auth sessions: cookie/session-based authentication implemented in `backend/app.py` ✅
* Deployment layer: frontend deployed on Vercel and backend deployed on Render with environment variable configuration and CORS handling ✅

### Deployment Status

* Frontend successfully deployed to Vercel:
  https://ai-expense-assistant-sepia.vercel.app/

* Backend successfully deployed to Render:
  https://ai-expense-assistant-cc.onrender.com

### Deployment Notes

* The deployed system supports authenticated multi-user usage through secure session cookies.
* Frontend and backend communicate through configured CORS policies.
* PostgreSQL-compatible deployment architecture is supported through `DATABASE_URL`.
* Environment variables are configured through the hosting platforms.
* The application is publicly accessible and supports live end-to-end receipt processing.

### After First Deliverable Goals

* Budgeting insights ✅ implemented.
  Implemented spending insight generation that analyzes receipt history and category spending patterns. Users receive personalized summaries and spending recommendations. Implemented in `backend/app.py`, `backend/db.py`, and displayed in `frontend/src/App.js`.

* Smarter category suggestions ✅ implemented
  GPT-4.1 Vision now automatically assigns categories to extracted receipt items during processing. Implemented in `backend/extractor.py`.

* Receipt search ✅ implemented.
  Users can search and filter receipt history by merchant name through the frontend search interface implemented in `frontend/src/App.js`.

* Receipt deletion ✅ implemented.
  Added ability to delete saved receipts from receipt history. Implemented through `DELETE /receipt/{id}` in `backend/app.py`, deletion logic in `backend/db.py`, and UI controls in `frontend/src/App.js`.

* Loading/progress feedback ✅ implemented.
  Added upload loading state and user feedback while receipt extraction is processing. Implemented in `frontend/src/App.js`.

* Non-receipt detection ✅ implemented.
  Added LLM-based receipt validation that rejects non-receipt uploads before extraction. Implemented in `backend/extractor.py` and upload handling in `backend/app.py`.

* Missing item editing ✅ implemented.
  Users can manually add missing receipt items after extraction and before saving corrections. Implemented in `frontend/src/App.js`.

* Recurring purchases ⚠️ not implemented.
  Identified during review as a valuable future feature. Due to project timeline constraints this feature was deferred to future work and documented in `REGRETS.md`.

* Trend charts ⚠️ partially implemented.
  Spending dashboards and category-spending visualizations are implemented using Recharts in `frontend/src/App.js`. Additional historical trend analysis and long-term spending projections remain future work.

### Notes

* No proposal items are marked as no longer planned.
* The deployed implementation remains aligned with the original proposal goals while extending the system with production deployment, authentication, and cost-management infrastructure.
