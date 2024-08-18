import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.sentry import models, schemas


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
