import os
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infra.database import get_db
from sqlalchemy import text

from authentification.routes import router as auth_router
from authentification.session import get_current_user
from infra.database import engine
from infra.models.audit import AuditEvent, OtpCode, RateLimit, UserSession
from infra.models.identity import (
    List_Service,
    Ongoing_Service,
    Permission,
    Picture,
    Users,
)


router = APIRouter(prefix="/api/services", tags=["services"])

@router.get("")
def get_service(db: Annotated[Session, Depends(get_db)]) -> dict:
    with engine.connect() as conn:

        test = {"db": conn.execute(text("SELECT * FROM list_service;")).scalar()}
        return test
