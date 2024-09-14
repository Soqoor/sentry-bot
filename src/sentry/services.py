import datetime
import json

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.sentry import models, schemas
from src.sentry.handlers.base import SentryHandlerFactory


class SentryService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_installation_id(self, installation_id: str) -> models.Installation | None:
        stmt = select(models.Installation).filter_by(installation_id=installation_id).limit(1)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create_or_update_installation(self, obj_in: schemas.InstallationCreateUpdate) -> models.Installation:
        db_installation = await self.get_by_installation_id(obj_in.installation_id)
        if db_installation:
            for key, value in obj_in.dict(exclude_unset=True).items():
                setattr(db_installation, key, value)
        else:
            db_installation = models.Installation(**obj_in.dict())
            self.db.add(db_installation)
        await self.db.commit()
        return db_installation

    async def new_installation_with_code(self, installation_id: str, code: str, org_slug: str):
        auth_token, refresh_token = await self._convert_installation_code(installation_id, code)
        installation = schemas.InstallationCreateUpdate(
            installation_id=installation_id,
            org_slug=org_slug,
            auth_token=auth_token,
            refresh_token=refresh_token,
        )
        await self.create_or_update_installation(installation)

    @staticmethod
    async def _convert_installation_code(installation_id: str, code: str):
        url = f"https://sentry.io/api/0/sentry-app-installations/{installation_id}/authorizations/"
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": settings.SENTRY_CLIENT_ID,
            "client_secret": settings.SENTRY_CLIENT_SECRET,
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload)
        data = resp.json()
        print(f"CONVERT TOKEN {data=}")
        auth_token = data["token"]
        refresh_token = data["refreshToken"]
        return auth_token, refresh_token

    async def log_sentry_activity(self, installation_id: str):
        db_installation = await self.get_by_installation_id(installation_id)
        if db_installation:
            db_installation.last_activity = datetime.datetime.now()
            db_installation.activity_counter = models.Installation.activity_counter + 1
            db_installation.is_active = True
            await self.db.commit()


class AlertService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_alert(self, obj_in: schemas.AlertCreate) -> None:
        db_alert = models.Alert(**obj_in.dict())
        self.db.add(db_alert)
        await self.db.commit()

    async def test_run(self, alert_ids_list: list) -> None:
        from src.bot.bot_application import bot_app

        # alert_ids_list = [int(i) for i in alert_ids_list]
        stmt = select(models.Alert).where(models.Alert.id.in_(alert_ids_list))
        result = await self.db.execute(stmt)
        for alert in result.scalars():
            handler = await SentryHandlerFactory(
                db=self.db,
                bot=bot_app,
                sentry_hook_resource=alert.sentry_hook_resource,
                update=json.loads(alert.update),
            ).get_handler()
            text = handler.create_alert_message()
            await bot_app.send_message(chat_id=settings.ADMIN_CHAT_ID, text=text)
