import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.chats import models, schemas


class ChatService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_or_update(self, chat: schemas.CreateOrUpdateChat):
        async with self.db as session:
            async with session.begin():
                stmt = select(models.Chat).filter_by(chat_id=chat.chat_id)
                result = await session.execute(stmt.limit(1))
                db_chat = result.scalars().first()
                if db_chat:
                    db_chat.last_activity = datetime.datetime.now()
                    db_chat.user_activity_counter += 1
                    db_chat.is_active = True
                    db_chat.username = chat.username
                    db_chat.first_name = chat.first_name
                    db_chat.last_name = chat.last_name
                    db_chat.chat_title = chat.chat_title
                else:
                    db_chat = models.Chat(**chat.dict())
                    session.add(db_chat)

    async def check_chat_slug(self, chat_slug: str) -> str | None:
        async with self.db as session:
            async with session.begin():
                stmt = select(models.Chat).filter_by(chat_slug=chat_slug)
                result = await session.execute(stmt.limit(1))
                db_chat = result.scalars().first()
                if not db_chat:
                    return "Chat with this slug does not exist"
                if not db_chat.is_active:
                    return "Bot have no rights to send messages to this chat"
                return
