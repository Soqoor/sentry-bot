from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.bot.routers import router as bot_router
from src.bot.services import BotService


@asynccontextmanager
async def lifespan(*args, **kwargs):
    BotService.setup_webhook()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(bot_router)
