# AI Expense Assistant — Design Decisions

## Overview

AI Expense Assistant is a deployed full-stack web application that allows authenticated users to upload receipt images, extract structured purchase information using OpenAI Vision models, edit extracted data, and analyze spending patterns through persistent dashboards.

Frontend deployment:

* Vercel
* https://ai-expense-assistant-sepia.vercel.app/

Backend deployment:

* Render
* https://ai-expense-assistant-cc.onrender.com

The application uses:

* React
* FastAPI
* PostgreSQL-compatible persistence
* OpenAI GPT-4.1 Vision
* cookie-based authentication
* spending analytics dashboards

This document focuses on three major design decisions made during development and explains the reasoning behind each decision, tradeoffs considered, and the degree of human vs AI involvement.

---

# Design Decision 1:

# Cookie-Based Authentication Instead of localStorage Tokens

## Decision

The application uses server-managed session cookies instead of storing authentication tokens in localStorage.

Authentication endpoints:

* `POST /register/`
* `POST /login/`
* `POST /logout/`
* `GET /me/`

The backend creates and validates session cookies, while the frontend uses Axios with `withCredentials: true`.

---

## Why This Decision Was Made

My original proposal planned to use localStorage session persistence because it was simpler to implement quickly.

However, proposal feedback from the course staff identified this as a security issue for a deployed application. The feedback specifically recommended:

* httpOnly cookies
* or a managed authentication provider

I decided to migrate to cookie-based authentication because:

* it was significantly more secure than localStorage tokens
* it still allowed me to implement the auth system myself
* it matched the “Ship with auth + live URL” requirement more appropriately

This required:

* configuring FastAPI cookie handling
* adding session tables to the database
* enabling credentialed CORS requests
* configuring secure cookie behavior in production
* updating frontend Axios configuration

---

## Tradeoffs

### Advantages

* Better protection against token theft through XSS
* More realistic production deployment architecture
* Sessions can be invalidated server-side
* Cleaner user authentication flow

### Disadvantages

* More difficult CORS configuration
* Harder deployment/debugging compared to localStorage
* Required backend session management
* Added complexity around cookie expiration and persistence

---

## Human vs AI Contribution

This decision was primarily human-driven.

I chose to redesign the authentication flow after reading the proposal feedback and understanding the deployment/security implications.

AI tools assisted with:

* debugging cookie/CORS issues
* generating implementation examples
* identifying FastAPI session configuration problems

However:

* the architectural decision to abandon localStorage
* the deployment/security reasoning
* and the integration plan

were decisions I made myself.

---

# Design Decision 2:

# PostgreSQL-Compatible Deployment Architecture

## Decision

The backend was designed to support:

* local SQLite development
* PostgreSQL-compatible production deployment through `DATABASE_URL`

The production deployment targets:

* Render backend hosting
* Vercel frontend hosting

The database layer dynamically switches between SQLite and Postgres depending on environment configuration.

---

## Why This Decision Was Made

The original proposal suggested SQLite initially with optional Postgres later.

During proposal feedback, the course staff warned that:

* SQLite could become problematic in deployment environments
* hosted platforms often expect managed Postgres
* deployment persistence might fail with SQLite-only infrastructure

Because of this, I redesigned the backend database layer to support production-ready Postgres deployment while preserving SQLite for local development convenience.

This affected:

* SQLAlchemy configuration
* environment variable handling
* deployment setup
* migration logic
* README and DEMO instructions

---

## Tradeoffs

### Advantages

* More realistic production architecture
* Easier deployment on Render
* Better persistence guarantees
* Easier future scalability
* Cleaner separation between local and production environments

### Disadvantages

* Additional deployment complexity
* More environment variable configuration
* More difficult debugging during deployment
* Required migration compatibility considerations

---

## Human vs AI Contribution

This was a mixed human/AI design process.

I independently decided:

* to adopt Postgres compatibility
* to deploy on Render/Vercel
* and to restructure the deployment architecture after staff feedback

AI assistance helped:

* generate deployment boilerplate
* debug environment variable issues
* troubleshoot CORS and backend deployment failures
* identify database configuration mistakes

The overall architecture and deployment direction were still decisions I made myself.

---

# Design Decision 3:

# Human-in-the-Loop Receipt Correction Workflow

## Decision

The system intentionally allows users to manually edit AI-extracted receipt data before saving receipts permanently.

The workflow is:

1. Upload receipt
2. AI extracts structured JSON
3. User reviews/edit fields
4. User saves corrected receipt
5. Corrected data persists in analytics/history

Editable fields include:

* merchant name
* totals
* dates
* item categories
* item prices

---

## Why This Decision Was Made

Receipt OCR and multimodal extraction are inherently imperfect.

Instead of treating the AI output as fully authoritative, I wanted the system to:

* treat extraction as a draft
* keep users in control
* support correction workflows
* improve practical usability

This also aligned well with the original Assignment 2 receipt scanner architecture.

The correction workflow became central to:

* dashboard accuracy
* analytics quality
* future category suggestion improvements

This design also made the app feel more realistic because financial applications generally require user verification.

---

## Tradeoffs

### Advantages

* Higher final data quality
* Better user trust
* More resilient to OCR/LLM extraction errors
* Better analytics consistency

### Disadvantages

* Additional frontend complexity
* More state management
* Additional backend update endpoints
* More UI design work

---

## Human vs AI Contribution

This decision was mostly human-driven.

I specifically wanted:

* editable extraction workflows
* persistent correction handling
* and user-controlled verification

because I felt that fully automated extraction would be unreliable for real usage.

AI tools mainly assisted with:

* React state management code
* UI formatting improvements
* debugging update endpoints
* implementation speed

The actual workflow design and user interaction model came from my own planning.

---

# Additional Design Considerations

## Cost Guardrails

The application includes:

* per-user monthly spending ceilings
* global daily OpenAI spending ceilings

This protects the deployment from runaway API usage and reflects production-oriented system design.

---

## Deployment Separation

The frontend and backend are deployed separately:

* Vercel for React frontend
* Render for FastAPI backend

This separation required:

* explicit CORS configuration
* environment variable management
* credentialed requests
* deployment debugging

but better reflects real-world hosted architectures.

---

# Current Status

Implemented:

* deployed frontend/backend
* secure cookie auth
* receipt upload and extraction
* editable correction workflow
* receipt persistence
* spending analytics dashboards
* production deployment configuration

Planned future work:

* budgeting insight generation
* recurring purchase detection
* trend analytics
* smarter category prediction
* receipt search/filtering

---

# Reflection

One of the biggest lessons from this project was that deployment and authentication complexity became much larger challenges than the AI extraction itself.

Most debugging time during deployment involved:

* CORS policies
* cookies/sessions
* environment variables
* password hashing
* frontend/backend integration

rather than the OpenAI extraction pipeline.

The project evolved significantly from the original Assignment 2 receipt scanner into a more production-oriented deployed system with stronger authentication and deployment architecture decisions.