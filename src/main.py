from contextlib import asynccontextmanager
from typing import TypedDict

import sentry_sdk
from aiogram import Bot, Dispatcher
from fastapi import FastAPI

from src.bot.bot_application import bot_app, bot_dp
from src.bot.routers import router as bot_router
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
    bot_app: Bot
    bot_dp: Dispatcher


@asynccontextmanager
async def lifespan(*args, **kwargs):
    r = await bot_app.set_webhook(
        url=f"https://{settings.DOMAIN}/telegram/",
        secret_token=settings.TG_SECRET_TOKEN,
    )
    print(f"{r=}")
    yield {
        "bot_app": bot_app,
        "bot_dp": bot_dp,
    }


app = FastAPI(lifespan=lifespan)

app.include_router(bot_router)
app.include_router(sentry_router)
