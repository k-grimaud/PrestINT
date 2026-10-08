import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, func, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from infra.database import Base


class Association(Base):
    __tablename__ = "association"
    asso_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(15))


class Users(Base):
    __tablename__ = "users"
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    __table_args__ = (Index("ux_users_email_lower", func.lower(email), unique=True),)


class Permission(Base):
    __tablename__ = "permission"
    asso_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("association.asso_id"), primary_key=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.user_id"), primary_key=True
    )
    permission: Mapped[str] = mapped_column(String(15))


class Picture(Base):
    __tablename__ = "picture"
    picture_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    asso_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("association.asso_id"))
    path: Mapped[str] = mapped_column(String(512))


class List_Service(Base):
    __tablename__ = "list_service"
    list_service_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    asso_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("association.asso_id"))
    approximative_cost: Mapped[int] = mapped_column(Integer)
    approximative_time: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(String(512))


class Ongoing_Service(Base):
    __tablename__ = "ongoing_service"
    service_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    asso_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("association.asso_id"))
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"))
    type_presta_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("list_service.list_service_id")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(25))
    context: Mapped[str] = mapped_column(String(255))
