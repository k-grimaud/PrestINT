import os
import uuid
from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Cookie,
    Depends,
    HTTPException,
    Request,
    Response,
)
from pydantic import BaseModel, StringConstraints
from sqlalchemy.orm import Session


@router.get("/me")
def me(user: Annotated[Users]) -> dict:
    return {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
