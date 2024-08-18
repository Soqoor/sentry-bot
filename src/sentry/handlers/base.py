import json
from abc import ABC, abstractmethod

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from src.sentry.schemas import InstallationCreateUpdate
from src.sentry.services import SentryService


class BaseSentryHandler(ABC):

    def __init__(self, db: AsyncSession, bot: Bot, update: dict):
        self.db = db
        self.bot = bot
        self.update = update

    @abstractmethod
    async def handle(self):
        pass


class SetupSentryHandler(BaseSentryHandler):

    async def handle(self):
        action = self.update.get("action")
        is_active = True if action == "created" else False
        await SentryService(db=self.db).create_or_update_installation(
            InstallationCreateUpdate(
                installation_id=self.update["data"]["installation"]["uuid"],
                org_slug=self.update["data"]["installation"]["organization"]["slug"],
                is_active=is_active,
            )
        )


class SentryHandlerFactory(BaseSentryHandler):

    async def get_handler(self) -> BaseSentryHandler:
        from src.sentry.handlers.alert import AlertSentryHandler
        from src.sentry.handlers.metric import MetricSentryHandler

        action = self.update.get("action")
        match action:
            case "created" | "deleted":
                handler = SetupSentryHandler
            case "triggered":
                handler = AlertSentryHandler
            case "critical" | "warning" | "resolved":
                handler = MetricSentryHandler
            case _:
                raise NotImplementedError(
                    f"Sentry handler factory is not implemented for {action} action.",
                    json.dumps(self.update, indent=4),
                )
        return handler(db=self.db, bot=self.bot, update=self.update)

    async def handle(self):
        pass
