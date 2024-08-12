import json

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.sentry import models, schemas


class SentryService:

    def __init__(self, db: AsyncSession, sentry_alert_dict: dict = None):
        self.db = db
        self.sentry_alert_dict = sentry_alert_dict

    async def handle_sentry_alert(self):
        match self.sentry_alert_dict.get("action"):
            case "created":
                await self._create_or_update_installation(
                    schemas.CreateOrUpdateInstallation(
                        installation_id=self.sentry_alert_dict["data"]["installation"]["uuid"],
                        org_slug=self.sentry_alert_dict["data"]["installation"]["organization"]["slug"],
                    )
                )
            case "deleted":
                await self._disable_installation(self.sentry_alert_dict["data"]["installation"]["uuid"])
            case _:
                raise NotImplementedError(json.dumps(self.sentry_alert_dict, indent=4))

    async def new_installation(self, installation_id: str, code: str, org_slug: str):
        auth_token, refresh_token = await self._convert_installation_code(installation_id, code)
        installation = schemas.CreateOrUpdateInstallation(
            installation_id=installation_id,
            org_slug=org_slug,
            auth_token=auth_token,
            refresh_token=refresh_token,
        )
        await self._create_or_update_installation(installation)

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

    async def _create_or_update_installation(
        self, installation: schemas.CreateOrUpdateInstallation
    ) -> models.Installation:
        async with self.db as session:
            async with session.begin():
                stmt = select(models.Installation).filter_by(installation_id=installation.installation_id)
                result = await session.execute(stmt.limit(1))
                db_installation = result.scalars().first()
                if db_installation:
                    db_installation.org_slug = installation.org_slug
                    db_installation.auth_token = installation.auth_token or db_installation.auth_token
                    db_installation.refresh_token = installation.refresh_token or db_installation.refresh_token
                else:
                    db_installation = models.Installation(**installation.dict())
                    session.add(db_installation)
        await session.refresh(db_installation)
        return db_installation

    async def _disable_installation(self, installation_id: str):
        async with self.db as session:
            async with session.begin():
                stmt = select(models.Installation).filter_by(installation_id=installation_id)
                result = await session.execute(stmt.limit(1))
                db_installation = result.scalars().first()
                if db_installation:
                    db_installation.is_active = False
