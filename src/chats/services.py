import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.chats import models, schemas


class ChatService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_chat_id(self, chat_id: int) -> models.Chat | None:
        stmt = select(models.Chat).filter_by(chat_id=chat_id).limit(1)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_chat_slug(self, chat_slug: str) -> models.Chat | None:
        stmt = select(models.Chat).filter_by(chat_slug=chat_slug).limit(1)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def log_chat_activity(self, chat: schemas.CreateOrUpdateChat):
        db_chat = await self.get_by_chat_id(chat.chat_id)
        if db_chat:
            db_chat.last_activity = datetime.datetime.now()
            db_chat.user_activity_counter = models.Chat.user_activity_counter + 1
            db_chat.is_active = True
            db_chat.username = chat.username
            db_chat.first_name = chat.first_name
            db_chat.last_name = chat.last_name
            db_chat.chat_title = chat.chat_title
        else:
            self.db.add(models.Chat(**chat.dict()))
        await self.db.commit()

    async def log_sentry_activity(self, chat_slug: str):
        db_chat = await self.get_by_chat_slug(chat_slug)
        if db_chat:
            db_chat.last_activity = datetime.datetime.now()
            db_chat.notify_activity_counter = models.Chat.notify_activity_counter + 1
            db_chat.is_active = True
            await self.db.commit()
