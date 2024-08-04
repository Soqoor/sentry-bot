from enum import Enum

from sqlalchemy import Boolean, DateTime
from sqlalchemy import Enum as SQLA_Enum
from sqlalchemy import Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class ChatTypeEnum(Enum):
    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"


class Chat(Base):
    __tablename__ = "chats"

    # pk and analytics
    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    last_activity: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    user_activity_counter: Mapped[int] = mapped_column(Integer, default=0)
    notify_activity_counter: Mapped[int] = mapped_column(Integer, default=0)

    # telegram properties
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    chat_type: Mapped[str] = mapped_column(SQLA_Enum(ChatTypeEnum))
    chat_id: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    chat_title: Mapped[str] = mapped_column(String)
    chat_inviter: Mapped[int] = mapped_column(Integer)
