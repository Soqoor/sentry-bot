from functools import wraps

from src.chats import schemas
from src.chats.services import ChatService
from src.database import get_db


def with_db_session(handler):
    @wraps(handler)
    async def wrapper(update, context, *args, **kwargs):
        db = await get_db().__anext__()
        chat = schemas.CreateOrUpdateChat(
            chat_id=update.effective_chat.id,
            chat_type=update.effective_chat.type,
            username=update.effective_user.username or "",
            first_name=update.effective_user.first_name or "",
            last_name=update.effective_user.last_name or "",
            chat_title=update.effective_chat.title or "",
            chat_inviter=update.effective_user.id,
        )
        await ChatService(db).create_or_update(chat)
        result = await handler(update, context, db, *args, **kwargs)
        return result

    return wrapper
