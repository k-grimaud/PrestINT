"""
Minimal script to test the stack (empty main.py --> crash) and check whether psql is up or not
"""

import os

from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()
engine = create_engine(os.environ["DATABASE_URL"])


@app.get("/api/health")
def health():
    with engine.connect() as conn:
        return {"db": conn.execute(text("SELECT 1")).scalar()}
