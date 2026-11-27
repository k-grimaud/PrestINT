import os
from typing import Annotated

from fastapi import Depends, FastAPI
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

app = FastAPI(openapi_url="/openapi.json" if os.getenv("DEV_DOCS") else None)
app.include_router(auth_router)


@app.get("/service")
async def get_service():
    with engine.connect() as conn:

        test = {"db": conn.execute(text("SELECT * FROM list_service;")).scalar()}
        print("/n/n/n/n/n/n")
        print(test)
        print("/n/n/n/n/n/n")
        return test
