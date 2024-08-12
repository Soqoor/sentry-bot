from pydantic import BaseModel

from src.chats.models import ChatTypeEnum


class CreateOrUpdateChat(BaseModel):
    chat_type: ChatTypeEnum
    chat_id: int
    username: str
    first_name: str
    last_name: str
    chat_title: str
    chat_inviter: int
