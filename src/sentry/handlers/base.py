from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession


class BaseSentryHandler:

    def __init__(self, db: AsyncSession, bot: Bot, sentry_hook_resource: str, update: dict):
        self.db = db
        self.bot = bot
        self.sentry_hook_resource = sentry_hook_resource
        self.update = update

    async def handle(self):
        raise NotImplementedError()


class SentryHandlerFactory(BaseSentryHandler):

    async def get_handler(self) -> BaseSentryHandler | None:
        from src.sentry.handlers.alert import EventAlertSentryHandler, MetricAlertSentryHandler
        from src.sentry.handlers.setup import SetupSentryHandler

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
