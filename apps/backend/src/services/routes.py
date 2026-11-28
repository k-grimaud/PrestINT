from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from authentification.session import get_current_user
from infra.database import engine, get_db
from infra.models.identity import List_Service, Users

from .services import EDIT_ROLES, READ_ROLES, get_user_role
from .template import Template

DB = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[Users, Depends(get_current_user)]


def service_reader(list_service_id: int, user: CurrentUser, db: DB) -> List_Service:
    service = db.get(List_Service, list_service_id)

    if service is None:
        raise HTTPException(404)
    if get_user_role(db, user.user_id, service.asso_id) not in READ_ROLES:
        raise HTTPException(403)

    return service


def service_editor(list_service_id: int, user: CurrentUser, db: DB) -> List_Service:
    service = db.get(List_Service, list_service_id)

    if service is None:
        raise HTTPException(404)
    if get_user_role(db, user.user_id, service.asso_id) not in EDIT_ROLES:
        raise HTTPException(403)

    return service


ServiceReader = Annotated[List_Service, Depends(service_reader)]
ServiceEditor = Annotated[List_Service, Depends(service_editor)]
router = APIRouter(prefix="/api/services", tags=["services"])


@router.get("")
def get_service(db: DB) -> dict:
    with engine.connect() as conn:

        test = {"db": conn.execute(text("SELECT * FROM list_service;")).scalar()}
        return test


@router.get("/{list_service_id}/template")
def get_template(service: ServiceReader) -> list[dict]:
    return service.template


@router.put("/{list_service_id}/template")
def put_template(service: ServiceEditor, body: Template, db: DB) -> None:
    service.template = [step.model_dump(mode="json") for step in body.steps]
    db.commit()
