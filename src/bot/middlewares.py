from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from src.chats import schemas
from src.chats.services import ChatService
from src.database import LocalSession


class DBSessionMiddleware(BaseMiddleware):

    async def __call__(
        self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]
    ) -> Any:
        async with LocalSession() as session:
            data["db"] = session
            return await handler(event, data)


class LogUserActivityMiddleware(BaseMiddleware):

    async def __call__(
        self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]
    ) -> Any:
        async with LocalSession() as session:
            chat = schemas.CreateOrUpdateChat(
                chat_id=event.chat.id,
                chat_type=event.chat.type,
                username=event.chat.username or "",
                first_name=event.chat.first_name or "",
                last_name=event.chat.last_name or "",
                chat_title=event.chat.title or "",
                chat_inviter=event.from_user.id,
            )
            await ChatService(session).log_chat_activity(chat)
        return await handler(event, data)
