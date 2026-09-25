"""
"""

import os
import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Cookie, Depends, HTTPException, Request, Response
from pydantic import BaseModel, StringConstraints
from sqlalchemy.orm import Session

from authentification.otp import OTP_LEN, request_otp, verify_otp
from authentification.session import SESSION_COOKIE, SESSION_TTL, create_session, get_current_user, revoke_session
from infra.database import get_db
from infra.models.identity import Users
from mail.mailer import send_otp_mail


TSP_MAIL = Annotated[str, StringConstraints(
    strip_whitespace=True, to_lower=True,
    pattern=r"^[a-z]+(?:-[a-z]+)*\.[a-z]+(?:-[a-z]+)*@telecom-sudparis\.eu$")]
OTP_CODE = Annotated[str, StringConstraints(strip_whitespace=True, pattern=rf"^\d{{{OTP_LEN}}}$")]
DB = Annotated[Session, Depends(get_db)]
# Secure cookies need https; dev runs over plain http, so .env sets COOKIE_SECURE=0 there
COOKIE_OPTS = dict(path="/", httponly=True, secure=os.getenv("COOKIE_SECURE", "1") != "0", samesite="lax")
router = APIRouter(prefix="/api/auth", tags=["auth"])


class OtpRequest(BaseModel):
    email: TSP_MAIL

class OtpVerify(BaseModel):
    email: TSP_MAIL
    code: OTP_CODE


@router.post("/otp/request", status_code=204)
def otp_request(body: OtpRequest, request: Request, background: BackgroundTasks, db: DB) -> None:
    """
    """

    code = request_otp(db, body.email, request.client.host)

    if code is not None:
        background.add_task(send_otp_mail, body.email, code)

@router.post("/otp/verify", status_code=204)
def otp_verify(body: OtpVerify, request: Request, response: Response, db: DB) -> None:
    """
    Verifies if the user gave the correct credential.
    Creates a session and store it in a Cookie if it is the case and throws Err 400 otherwise
    """

    user = verify_otp(db, body.email, body.code, request.client.host)

    if user is None:
        raise HTTPException(400, "Invalid or expired code")

    session_id = create_session(db, user.user_id)
    response.set_cookie(SESSION_COOKIE, str(session_id), max_age=int(SESSION_TTL.total_seconds()), **COOKIE_OPTS)


@router.post("/logout", status_code=204)
def logout(response: Response, db: DB, session: Annotated[str | None, Cookie()] = None) -> None:
    """
    """

    try:
        revoke_session(db, uuid.UUID(session))
    except (TypeError, ValueError):
        pass

    response.delete_cookie(SESSION_COOKIE, **COOKIE_OPTS)

@router.get("/me")
def me(user: Annotated[Users, Depends(get_current_user)]) -> dict:
    """
    """

    return {"email": user.email, "first_name": user.first_name, "last_name": user.last_name}
