from contextlib import asynccontextmanager
from typing import TypedDict

import sentry_sdk
from fastapi import FastAPI
from telegram.ext import Application

from src.bot.bot_application import get_bot_application
from src.bot.routers import router as bot_router
from src.bot.services import setup_webhook
from src.config import settings
from src.sentry.routers import router as sentry_router

if settings.SENTRY_ENABLED:
    sentry_sdk.init(
        dsn=settings.SENTRY_DNS,
        environment=settings.SENTRY_ENV,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )


class State(TypedDict):
    bot_app: Application


@asynccontextmanager
async def lifespan(*args, **kwargs):
    await setup_webhook()
    bot_app = await get_bot_application()
    yield {"bot_app": bot_app}


app = FastAPI(lifespan=lifespan)

app.include_router(bot_router)
app.include_router(sentry_router)
