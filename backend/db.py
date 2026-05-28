import os
import json
import datetime
import secrets
from typing import Optional

from dotenv import load_dotenv
from passlib.context import CryptContext
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    Boolean,
    select,
    insert,
    update,
    delete,
    func,
    text,
)
from sqlalchemy.exc import IntegrityError

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "../data/app.db")
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DB_FILE}").strip()
CORRECTIONS_FILE = os.path.join(BASE_DIR, "../data/corrections.json")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, future=True)
else:
    engine = create_engine(DATABASE_URL, future=True)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False, unique=True),
    Column("password_hash", String, nullable=False),
)

sessions = Table(
    "sessions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("token", String, nullable=False, unique=True),
    Column("expires_at", DateTime, nullable=False),
)

receipts = Table(
    "receipts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("store_name", String),
    Column("date", String),
    Column("total", Float),
    Column("raw_json", Text),
    Column("user_id", Integer, nullable=False),
    Column("estimated_cost", Float, default=0.0),
    Column("created_at", DateTime, nullable=False),
    Column("draft", Boolean, nullable=False, default=True),
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

GLOBAL_DAILY_COST_CEILING = float(os.environ.get("GLOBAL_DAILY_COST_CEILING", "10.0"))
USER_MONTHLY_COST_CEILING = float(os.environ.get("USER_MONTHLY_COST_CEILING", "5.0"))
SESSION_DURATION_DAYS = int(os.environ.get("SESSION_DURATION_DAYS", "7"))


def init_db():
    metadata.create_all(engine)
    _migrate_existing_schema()


def _pragma_columns(table_name: str) -> list[str]:
    with engine.connect() as conn:
        result = conn.execute(text(f"PRAGMA table_info({table_name})"))
        return [row[1] for row in result]


def _migrate_existing_schema() -> None:
    if DATABASE_URL.startswith("sqlite"):
        with engine.begin() as conn:
            users_columns = _pragma_columns("users")
            if "password_hash" not in users_columns:
                conn.execute(text("ALTER TABLE users ADD COLUMN password_hash TEXT"))
                if "password" in users_columns:
                    rows = conn.execute(text("SELECT id, password FROM users")).all()
                    for row in rows:
                        user_id, password = row
                        if password:
                            hashed = hash_password(password)
                            conn.execute(
                                update(users)
                                .where(users.c.id == user_id)
                                .values(password_hash=hashed)
                            )
            receipts_columns = _pragma_columns("receipts")
            if "estimated_cost" not in receipts_columns:
                conn.execute(text("ALTER TABLE receipts ADD COLUMN estimated_cost FLOAT DEFAULT 0.0"))
                conn.execute(text("UPDATE receipts SET estimated_cost = 0.0 WHERE estimated_cost IS NULL"))
            if "created_at" not in receipts_columns:
                conn.execute(text("ALTER TABLE receipts ADD COLUMN created_at DATETIME"))
                conn.execute(text("UPDATE receipts SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL"))
            if "draft" not in receipts_columns:
                conn.execute(text("ALTER TABLE receipts ADD COLUMN draft BOOLEAN DEFAULT 1"))
                conn.execute(text("UPDATE receipts SET draft = 1 WHERE draft IS NULL"))


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_user(username: str, password: str) -> Optional[int]:
    password_hash = hash_password(password)
    with engine.begin() as conn:
        try:
            result = conn.execute(
                insert(users).values(username=username, password_hash=password_hash)
            )
            return int(result.inserted_primary_key[0])
        except IntegrityError:
            return None


def authenticate_user(username: str, password: str) -> Optional[dict]:
    with engine.connect() as conn:
        row = conn.execute(select(users).where(users.c.username == username)).first()
        if row is None:
            return None
        if verify_password(password, row.password_hash):
            return {"id": row.id, "username": row.username}
        return None


def create_session(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=SESSION_DURATION_DAYS)
    with engine.begin() as conn:
        conn.execute(
            insert(sessions).values(user_id=user_id, token=token, expires_at=expires_at)
        )
    return token


def delete_session(token: str) -> None:
    with engine.begin() as conn:
        conn.execute(delete(sessions).where(sessions.c.token == token))


def get_user_by_session(token: str) -> Optional[dict]:
    if not token:
        return None
    with engine.begin() as conn:
        row = conn.execute(select(sessions).where(sessions.c.token == token)).first()
        if row is None:
            return None
        if row.expires_at < datetime.datetime.utcnow():
            conn.execute(delete(sessions).where(sessions.c.token == token))
            return None
        user_row = conn.execute(select(users).where(users.c.id == row.user_id)).first()
        if user_row is None:
            return None
        return {"id": user_row.id, "username": user_row.username}


def save_draft_receipt(data: dict, user_id: int, estimated_cost: float) -> int:
    with engine.begin() as conn:
        result = conn.execute(
            insert(receipts).values(
                store_name=data.get("store_name"),
                date=data.get("date"),
                total=float(data.get("total", 0) or 0),
                raw_json=json.dumps(data),
                user_id=user_id,
                estimated_cost=estimated_cost,
                created_at=datetime.datetime.utcnow(),
                draft=True,
            )
        )
        return int(result.inserted_primary_key[0])


def update_receipt(receipt_id: int, user_id: int, data: dict) -> bool:
    with engine.begin() as conn:
        result = conn.execute(
            update(receipts)
            .where(receipts.c.id == receipt_id, receipts.c.user_id == user_id)
            .values(
                store_name=data.get("store_name"),
                date=data.get("date"),
                total=float(data.get("total", 0) or 0),
                raw_json=json.dumps(data),
                draft=False,
            )
        )
        return result.rowcount > 0


def get_receipts(user_id: int) -> list[dict]:
    with engine.connect() as conn:
        rows = conn.execute(
            select(receipts)
            .where(receipts.c.user_id == user_id, receipts.c.draft == False)
            .order_by(receipts.c.id.desc())
        ).all()

    return [
        {
            "id": row.id,
            "store_name": row.store_name,
            "date": row.date,
            "total": row.total,
            "estimated_cost": row.estimated_cost,
            "data": json.loads(row.raw_json or "{}"),
        }
        for row in rows
    ]


def get_summary(user_id: int) -> list[dict]:
    with engine.connect() as conn:
        rows = conn.execute(
            select(receipts.c.store_name, func.sum(receipts.c.total).label("total"))
            .where(receipts.c.user_id == user_id, receipts.c.draft == False)
            .group_by(receipts.c.store_name)
        ).all()
    return [{"store": row.store_name, "total": float(row.total or 0)} for row in rows]


def get_category_summary(user_id: int) -> dict:
    with engine.connect() as conn:
        rows = conn.execute(
            select(receipts.c.raw_json)
            .where(receipts.c.user_id == user_id, receipts.c.draft == False)
        ).all()

    category_totals: dict[str, float] = {}
    for (raw_json,) in rows:
        try:
            data = json.loads(raw_json or "{}")
        except json.JSONDecodeError:
            continue
        for item in data.get("items", []):
            cat = item.get("category") or "Unknown"
            total = float(item.get("total_price", 0) or 0)
            category_totals[cat] = category_totals.get(cat, 0) + total

    return category_totals


def get_receipt_by_id(receipt_id: int, user_id: int) -> Optional[dict]:
    with engine.connect() as conn:
        row = conn.execute(
            select(receipts).where(receipts.c.id == receipt_id, receipts.c.user_id == user_id)
        ).first()
    if row is None:
        return None
    return {
        "id": row.id,
        "store_name": row.store_name,
        "date": row.date,
        "total": row.total,
        "estimated_cost": row.estimated_cost,
        "data": json.loads(row.raw_json or "{}"),
        "draft": bool(row.draft),
    }


def _parse_date(value):
    if isinstance(value, datetime.datetime):
        return value
    try:
        return datetime.datetime.fromisoformat(value)
    except Exception:
        return None


def get_user_monthly_cost(user_id: int) -> float:
    now = datetime.datetime.utcnow()
    with engine.connect() as conn:
        rows = conn.execute(
            select(receipts.c.estimated_cost, receipts.c.created_at).where(receipts.c.user_id == user_id)
        ).all()
    total = 0.0
    for row in rows:
        created_at = _parse_date(row.created_at)
        if created_at and created_at.year == now.year and created_at.month == now.month:
            total += float(row.estimated_cost or 0)
    return total


def get_global_daily_cost() -> float:
    now = datetime.datetime.utcnow()
    with engine.connect() as conn:
        rows = conn.execute(select(receipts.c.estimated_cost, receipts.c.created_at)).all()
    total = 0.0
    for row in rows:
        created_at = _parse_date(row.created_at)
        if created_at and created_at.date() == now.date():
            total += float(row.estimated_cost or 0)
    return total


def load_corrections() -> dict:
    try:
        with open(CORRECTIONS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"merchant_aliases": {}, "item_categories": {}}


def save_corrections(corrections: dict) -> None:
    with open(CORRECTIONS_FILE, "w") as f:
        json.dump(corrections, f, indent=2)
