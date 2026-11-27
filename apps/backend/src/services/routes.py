from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from infra.database import engine, get_db

router = APIRouter(prefix="/api/services", tags=["services"])


@router.get("")
def get_service(db: Annotated[Session, Depends(get_db)]) -> dict:
    with engine.connect() as conn:

        test = {"db": conn.execute(text("SELECT * FROM list_service;")).scalar()}
        return test
