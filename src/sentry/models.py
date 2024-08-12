import uuid
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


def uuid_generator():
    return str(uuid.uuid4())


class Installation(Base):
    __tablename__ = "installations"

    id: Mapped[int] = mapped_column(primary_key=True)
    installation_id: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    org_slug: Mapped[str] = mapped_column(String)
    auth_token: Mapped[str] = mapped_column(String)
    refresh_token: Mapped[str] = mapped_column(String)
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("chats.id"), nullable=True)
