# AI Expense Assistant
### “AI-powered receipt scanner with budgeting insights and recurring spending analysis (Ship with auth + live URL)”

---

# One Sentence Description

An AI-powered expense tracking web app that allows users to upload receipts, automatically extract structured purchase information using multimodal LLMs, track spending patterns over time, and receive AI-generated budgeting insights through a deployed authenticated web application.

---

# Past Project Reference

This project extends Assignment 2: Document Scanner (Receipt Scanner).

Base project repository:  
https://github.com/ucsd-cse-genai-programming-sp26/02-doc-scanner-cc

The current system already supports:
- receipt upload
- multimodal receipt extraction using GPT-4.1
- user correction workflows
- persistent receipt history
- spending dashboards
- basic authentication and per-user data isolation

This final project will extend the system into a more complete AI expense assistant with deployment, budgeting insights, and enhanced analytics.

---

# Planned Technologies

## Frontend
- React
- Axios
- Recharts

## Backend
- FastAPI
- Python

## Database
- SQLite (initially)
- Optional PostgreSQL if deployment requires it

## AI / LLM
- OpenAI GPT-4.1 Vision API

## Authentication
- Existing username/password auth system
- Session persistence using localStorage

## Deployment
Potential options:
- Render
- Railway
- Fly.io

## Other Tools
- dotenv
- uvicorn

---

# First Deliverable

## Goal
Deploy the existing receipt scanner as a live authenticated web application.

## User Story
A user should be able to:
1. Create an account
2. Login
3. Upload a receipt
4. Edit extracted data
5. Save the receipt
6. View their own spending dashboard
7. Access the app from a public URL

## Why This Deliverable
This forces every major system component to work together:
- frontend
- backend API
- authentication
- database persistence
- AI extraction
- deployment
- networking/configuration

It validates the full stack before adding more advanced AI assistant features.

---

# Rough Architecture for First Deliverable

## 1. React Frontend
### Input
- Receipt image upload
- Login credentials
- User corrections

### Output
- Dashboard UI
- Editable extracted receipt data
- Spending analytics

### Effects
- Sends API requests to backend
- Maintains user session state

---

## 2. FastAPI Backend
### Input
- Uploaded images
- Authentication requests
- Corrected receipt data

### Output
- Structured JSON receipt data
- Aggregated summaries
- Auth responses

### Effects
- Calls OpenAI API
- Reads/writes database

---

## 3. Receipt Extraction Pipeline
### Input
- Receipt image bytes

### Output
Structured JSON:
```json
{
  "store_name": "...",
  "date": "...",
  "total": "...",
  "items": [...]
}

--- 

## 4. User Correction Memory 
### Input

- Corrected categories/store names

### Output 

- Updated correction mappings

### Effects

- Stores reusable extraction hints
- Injects corrections into future prompts

---

## 5. SQLite Database

### Stores

- Users
- Receipts
- Receipt metadata
- Per-user receipt history

### Effects

- Enables persistence across sessions
- Supports dashboard aggregation queries

---

## 6. Analytics Layer

### Input

- Stored receipt data

### Output

- Spending by store
- Spending by category
- Historical summaries

---

## 7. Deployment Layer

### Responsibilities

- Hosting frontend/backend
- Environment variable configuration
- Secure API key handling
- Public 

---

## After First Deliverable Goals

### AI Budgeting Insights

- Generate natural-language spending summaries
- Detect unusually high spending categories
- Suggest budget improvements

Example:

“You spent 32% more on dining this month compared to last month.”

---

## Recurring Purchase Detection

- Detect repeated merchants/subscriptions
- Highlight recurring expenses automatically

Examples:

- Netflix
- Spotify
- Gym memberships

---

## Monthly Spending Trends

* Line charts across weeks/months
* Category trend tracking over time

---

## Smarter Category Suggestions

- Use historical user corrections to auto-suggest categories
- Confidence-based category recommendations

---

## Receipt Search

Allow users to search receipts by:

- merchant
- item name
- category
- date range

---

## Improved Dashboard UX

- Better layout organization
- Mobile responsiveness
- Cleaner analytics views