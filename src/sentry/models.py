import uuid
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


def uuid_generator():
    return str(uuid.uuid4())


class Installation(Base):
    __tablename__ = "installations"

    # analytics
    last_activity: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)
    activity_counter: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    installation_id: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    org_slug: Mapped[str] = mapped_column(String(255))
    auth_token: Mapped[str] = mapped_column(String(255))
    refresh_token: Mapped[str] = mapped_column(String(255))
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("chats.id"), nullable=True)


class Alert(Base):
    __tablename__ = "alerts"

    title: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    sentry_hook_resource: Mapped[str] = mapped_column(String(32))
    update: Mapped[str] = mapped_column(String)
    error_message: Mapped[Optional[str]] = mapped_column(String(255))
