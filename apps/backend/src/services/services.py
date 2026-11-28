from typing import Literal
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from infra.models.identity import Permission

Role = Literal["org_admin", "org_member", "org_viewer"]
READ_ROLES: set[Role] = {"org_admin", "org_member"}
EDIT_ROLES: set[Role] = {"org_admin"}


def get_user_role(db: Session, user_id: UUID, asso_id: str) -> Role | None:
    """
    Return the role of the given user for the given association.
    A user not registered to the association will have permission None
    """
    permission = db.scalar(
        select(Permission.permission).where(
            Permission.user_id == user_id,
            Permission.asso_id == asso_id,
        )
    )

    return permission
