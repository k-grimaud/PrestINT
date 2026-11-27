import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from infra.database import Base


class Message(Base):
    __tablename__ = "message"
    message_id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("ongoing_service.service_id"))
    sender_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"))
    message: Mapped[str] = mapped_column(String(1000))
    delivered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
