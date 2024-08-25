from abc import ABC, abstractmethod

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from src.sentry.schemas import InstallationCreateUpdate
from src.sentry.services import SentryService


class BaseSentryHandler(ABC):

    def __init__(self, db: AsyncSession, bot: Bot, sentry_hook_resource: str, update: dict):
        self.db = db
        self.bot = bot
        self.sentry_hook_resource = sentry_hook_resource
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

    async def get_handler(self) -> BaseSentryHandler | None:
        from src.sentry.handlers.alert import EventAlertSentryHandler
        from src.sentry.handlers.metric import MetricAlertSentryHandler

        action = self.sentry_hook_resource
        match action:
            case "installation":
                handler = SetupSentryHandler
            case "event_alert":
                handler = EventAlertSentryHandler
            case "metric_alert":
                handler = MetricAlertSentryHandler
            case _:
                return None
        return handler(db=self.db, bot=self.bot, sentry_hook_resource=self.sentry_hook_resource, update=self.update)

    async def handle(self):
        pass
