import os
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, text
from pydantic import BaseModel, StringConstraints


TSP_MAIL = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        to_lower=True,
        pattern=r"^[a-z]+(?:-[a-z]+)*\.[a-z]+(?:-[a-z]+)*@telecom-sudparis\.eu$"
    )
]


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class OtpRequest(BaseModel):
    email: TSP_MAIL


app = FastAPI(openapi_url="/openapi.json" if os.getenv("DEV_DOCS") else None)
engine = create_engine(os.environ["DATABASE_URL"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/api/health")
def health():
    """
    Minimal script to test the app
    """
    with engine.connect() as conn:
        return {"db": conn.execute(text("SELECT 1")).scalar()}

app.get("/auth/otp/request{email: TSP_MAIL}")
def request_email_otp(email: TSP_MAIL):
    pass

app.get("/auth/otp/verify{email: TSP_MAIL, code: str}")
def verify_token():
    pass

app.get("/auth/logout")
def logout_user():
    pass

@app.get("/items")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
