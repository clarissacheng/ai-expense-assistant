import os
import json
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Depends, Cookie, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.extractor import extract_receipt_data
from backend.db import (
    init_db,
    create_user,
    authenticate_user,
    create_session,
    delete_session,
    get_user_by_session,
    save_draft_receipt,
    update_receipt,
    delete_receipt as db_delete_receipt,
    get_summary,
    get_category_summary,
    get_receipts,
    get_user_monthly_cost,
    get_global_daily_cost,
    get_budget_insights,
    load_corrections,
    save_corrections,
    USER_MONTHLY_COST_CEILING,
    GLOBAL_DAILY_COST_CEILING,
)

app = FastAPI()

allowed_origins = [
    origin.strip() for origin in os.environ.get(
        "ALLOW_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000"
    ).split(",")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"

@app.on_event("startup")
def startup():
    print("Starting backend with CORS origins:", allowed_origins)
    init_db()


@app.exception_handler(Exception)
async def all_exception_handler(request, exc):
    import traceback
    print("Unhandled exception:", repr(exc))
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)},
    )


class AuthPayload(BaseModel):
    username: str
    password: str


def require_user(session_token: Optional[str] = Cookie(default=None)):
    user = get_user_by_session(session_token)
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

@app.post("/register/")
def register(data: AuthPayload):
    if not data.username or not data.password:
        raise HTTPException(status_code=400, detail="username and password are required")
    user_id = create_user(data.username, data.password)
    if user_id is None:
        raise HTTPException(status_code=400, detail="username already exists")
    return {"status": "registered"}

@app.post("/login/")
def login(data: AuthPayload):
    user = authenticate_user(data.username, data.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_session(user["id"])
    response = JSONResponse({"status": "ok"})
    # Use SameSite=None only when cookie is secure; otherwise use Lax for local dev
    samesite_val = "none" if COOKIE_SECURE else "lax"
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        samesite=samesite_val,
        secure=COOKIE_SECURE,
        max_age=7 * 24 * 60 * 60,
    )
    return response

@app.post("/logout/")
def logout(response: Response, session_token: Optional[str] = Cookie(default=None)):
    if session_token:
        delete_session(session_token)
    response = JSONResponse({"status": "logged_out"})
    response.delete_cookie("session_token")
    return response

@app.get("/me/")
def me(user: dict = Depends(require_user)):
    return {"user_id": user["id"], "username": user["username"]}

@app.post("/upload/")
async def upload(file: UploadFile = File(...), user: dict = Depends(require_user)):
    contents = await file.read()

    user_cost = get_user_monthly_cost(user["id"])
    global_cost = get_global_daily_cost()
    estimated_cost = 0.05

    if user_cost + estimated_cost > USER_MONTHLY_COST_CEILING:
        raise HTTPException(status_code=402, detail="Monthly API budget exceeded")
    if global_cost + estimated_cost > GLOBAL_DAILY_COST_CEILING:
        raise HTTPException(status_code=402, detail="Global daily API cost ceiling reached")

    result = extract_receipt_data(contents)
    if result.get("not_receipt"):
        raise HTTPException(status_code=400, detail="Uploaded file does not appear to be a receipt.")
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=500, detail=result["error"])
    if result.get("not_receipt"):
        raise HTTPException(status_code=400, detail="Uploaded image does not appear to be a receipt.")

    receipt_id = save_draft_receipt(result, user["id"], estimated_cost)
    return {"receipt_id": receipt_id, "data": result, "estimated_cost": estimated_cost}

@app.put("/receipt/{receipt_id}")
def save_receipt(receipt_id: int, data: dict, user: dict = Depends(require_user)):
    success = update_receipt(receipt_id, user["id"], data)
    if not success:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return {"status": "updated"}

@app.get("/summary/")
def summary(user: dict = Depends(require_user)):
    return get_summary(user["id"])

@app.get("/category_summary/")
def category_summary(user: dict = Depends(require_user)):
    return get_category_summary(user["id"])

@app.get("/receipts/")
def get_receipts_route(user: dict = Depends(require_user)):
    return get_receipts(user["id"])

@app.get("/costs/")
def cost_summary(user: dict = Depends(require_user)):
    return {
        "user_monthly_cost": get_user_monthly_cost(user["id"]),
        "user_monthly_limit": USER_MONTHLY_COST_CEILING,
        "global_daily_cost": get_global_daily_cost(),
        "global_daily_limit": GLOBAL_DAILY_COST_CEILING,
    }

@app.get("/budget_insights/")
def budget_insights(user: dict = Depends(require_user)):
    return get_budget_insights(user["id"])

@app.post("/correct/")
def correct(data: dict, user: dict = Depends(require_user)):
    corrections = load_corrections()

    if "store_name_original" in data and "store_name" in data:
        orig = data["store_name_original"]
        corrected = data["store_name"]
        if orig != corrected:
            corrections["merchant_aliases"][orig] = corrected

    if "items" in data:
        for item in data["items"]:
            if "name" in item and "category" in item:
                corrections["item_categories"][item["name"]] = item["category"]

    save_corrections(corrections)
    return {"status": "saved"}

@app.delete("/receipt/{receipt_id}")
def delete_receipt_route(receipt_id: int, user: dict = Depends(require_user)):
    success = db_delete_receipt(
        receipt_id,
        user["id"]
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Receipt not found"
        )

    return {"status": "deleted"}
