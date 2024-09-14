import random
import string
from enum import Enum
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime
from sqlalchemy import Enum as SQLA_Enum
from sqlalchemy import Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base
from src.utils import slugify


class ChatTypeEnum(Enum):
    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"


def chat_slug_generator(context):
    if context.get_current_parameters()["chat_type"] == ChatTypeEnum.PRIVATE:
        chat_slug = slugify(
            context.get_current_parameters()["username"]
            or context.get_current_parameters()["first_name"] + context.get_current_parameters()["last_name"]
        )
    else:
        chat_slug = slugify(context.get_current_parameters()["chat_title"])
    random_prefix = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"{chat_slug}-{random_prefix}".lower()


class Chat(Base):
    __tablename__ = "chats"

    # analytics
    last_activity: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)
    user_activity_counter: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    notify_activity_counter: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # telegram properties
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    chat_type: Mapped[str] = mapped_column(SQLA_Enum(ChatTypeEnum, length=10))
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(255))
    first_name: Mapped[Optional[str]] = mapped_column(String(255))
    last_name: Mapped[Optional[str]] = mapped_column(String(255))
    chat_title: Mapped[Optional[str]] = mapped_column(String(255))
    chat_inviter: Mapped[Optional[int]] = mapped_column(Integer)

    # sentry properties
    chat_slug: Mapped[str] = mapped_column(String(255), default=chat_slug_generator)

    @property
    def name_display(self) -> str:
        match self.chat_type:
            case ChatTypeEnum.PRIVATE:
                return self.username or self.first_name + self.last_name
            case ChatTypeEnum.GROUP | ChatTypeEnum.SUPERGROUP:
                return self.chat_title
            case _:
                raise NotImplementedError(f"Display name for {self.chat_type}")
