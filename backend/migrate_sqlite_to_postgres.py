#!/usr/bin/env python3
"""
Simple migration script to copy data from a local SQLite DB to a Postgres database.

Usage:
  TARGET_DATABASE_URL=postgresql://user:pass@host:5432/db python3 backend/migrate_sqlite_to_postgres.py
Optionally set SOURCE_DATABASE_URL to a different source (default: sqlite:///../data/app.db).

This script uses the table definitions in `backend.db` to create tables on the
target database and copies rows. It will attempt to normalize the `users`
password column into `password_hash` by hashing `password` where present.
"""
import os
import sys
from sqlalchemy import create_engine, text, inspect, insert

from backend import db as app_db

SOURCE = os.environ.get("SOURCE_DATABASE_URL", f"sqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/app.db'))}")
TARGET = os.environ.get("TARGET_DATABASE_URL") or os.environ.get("DATABASE_URL")

if not TARGET:
    print("ERROR: set TARGET_DATABASE_URL (or DATABASE_URL) to the Postgres target")
    sys.exit(1)

def make_engine(url: str):
    if url.startswith("sqlite"):
        return create_engine(url, connect_args={"check_same_thread": False}, future=True)
    return create_engine(url, future=True)

source_engine = make_engine(SOURCE)
target_engine = make_engine(TARGET)

print(f"Source: {SOURCE}")
print(f"Target: {TARGET}")

# Ensure target has tables
app_db.metadata.create_all(target_engine)

inspector = inspect(source_engine)

def fetch_all(table_name: str):
    with source_engine.connect() as conn:
        rows = conn.execute(text(f"SELECT * FROM {table_name}"))
        return [dict(row) for row in rows.mappings().all()]

def copy_users():
    src_cols = [c['name'] for c in inspector.get_columns('users')]
    rows = fetch_all('users')
    transformed = []
    for r in rows:
        payload = {
            'id': r.get('id'),
            'username': r.get('username'),
        }
        if 'password_hash' in r and r.get('password_hash'):
            payload['password_hash'] = r.get('password_hash')
        elif 'password' in r and r.get('password'):
            payload['password_hash'] = app_db.hash_password(r.get('password'))
        else:
            # create unusable password if missing
            payload['password_hash'] = app_db.hash_password("")
        transformed.append(payload)

    with target_engine.begin() as conn:
        for p in transformed:
            conn.execute(insert(app_db.users).values(**p))
    print(f"Copied {len(transformed)} users")

def copy_sessions():
    try:
        rows = fetch_all('sessions')
    except Exception:
        print('No sessions table found in source; skipping')
        return
    with target_engine.begin() as conn:
        for r in rows:
            payload = {
                'id': r.get('id'),
                'user_id': r.get('user_id'),
                'token': r.get('token'),
                'expires_at': r.get('expires_at'),
            }
            conn.execute(insert(app_db.sessions).values(**payload))
    print(f"Copied {len(rows)} sessions")

def copy_receipts():
    try:
        rows = fetch_all('receipts')
    except Exception:
        print('No receipts table found in source; skipping')
        return
    transformed = []
    for r in rows:
        payload = {
            'id': r.get('id'),
            'store_name': r.get('store_name'),
            'date': r.get('date'),
            'total': r.get('total'),
            'raw_json': r.get('raw_json'),
            'user_id': r.get('user_id'),
            'estimated_cost': r.get('estimated_cost') if 'estimated_cost' in r else 0.0,
            'created_at': r.get('created_at'),
            'draft': r.get('draft') if 'draft' in r else True,
        }
        transformed.append(payload)

    with target_engine.begin() as conn:
        for p in transformed:
            conn.execute(insert(app_db.receipts).values(**p))
    print(f"Copied {len(transformed)} receipts")

def main():
    copy_users()
    copy_sessions()
    copy_receipts()
    print('Migration complete')

if __name__ == '__main__':
    main()
