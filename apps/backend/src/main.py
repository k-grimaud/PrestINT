import os
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, text
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


app = FastAPI()
engine = create_engine(os.environ["DATABASE_URL"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/api/health")
def health():
    """
    Minimal script to test the app
    """
    with engine.connect() as conn:
        return {"db": conn.execute(text("SELECT 1")).scalar()}

@app.get("/items")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
