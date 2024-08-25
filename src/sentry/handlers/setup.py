from src.sentry.handlers.base import BaseSentryHandler
from src.sentry.schemas import InstallationCreateUpdate
from src.sentry.services import SentryService


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
