"""
"""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException
from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from infra.database import get_db
from infra.models.audit import UserSession
from infra.models.identity import Users


SESSION_COOKIE = "session"
SESSION_TTL = timedelta(days=1)


def create_session(db, user_id: uuid.UUID) -> uuid.UUID:
    """
    """

    session = UserSession(user_id=user_id, expires_at=datetime.now(timezone.utc) + SESSION_TTL)
    db.add(session)
    db.commit()

    return session.id

def get_current_user(db: Annotated[Session, Depends(get_db)], session: Annotated[str | None, Cookie()] = None) -> Users:
    """
    """

    # Checking for Cookie existence (aka the session ID)
    try:
        session_id = uuid.UUID(session)
    except (TypeError, ValueError):
        raise HTTPException(401)

    user = db.scalar(
        select(Users).join(UserSession, UserSession.user_id == Users.user_id).where(UserSession.id == session_id, UserSession.revoked_at.is_(None), UserSession.expires_at > func.now())
    )

    if user is None:
        raise HTTPException(401)

    return user

def revoke_session(db: Session, session_id: uuid.UUID):
    """
    Revokes the given session bind to the user
    """

    db.execute(update(UserSession).where(UserSession.id == session_id, UserSession.revoked_at.is_(None)).values(revoked_at=func.now()))
    db.commit()
