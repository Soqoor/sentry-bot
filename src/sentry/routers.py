from typing import cast

from aiogram import Bot
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.chats.services import ChatService
from src.config import settings
from src.database import get_db
from src.sentry.handlers.base import SentryHandlerFactory
from src.sentry.services import SentryService

router = APIRouter()


@router.get("/sentry/install/")
async def install_endpoint(code: str, installationId: str, orgSlug: str, db: AsyncSession = Depends(get_db)):
    await SentryService(db=db).new_installation_with_code(
        installation_id=installationId,
        org_slug=orgSlug,
        code=code,
    )
    return RedirectResponse(f"https://t.me/{settings.TG_BOT_NAME}?start={installationId}")


@router.post("/sentry/alert-rule")
async def alert_rule_endpoint(update_dict: dict, db: AsyncSession = Depends(get_db)):
    chat_slug = update_dict.get("fields")[0].get("value")
    chat = await ChatService(db).get_by_chat_slug(chat_slug)
    if not chat:
        return JSONResponse(status_code=400, content={"message": "Chat with this slug does not exist"})
    if not chat.is_active:
        return JSONResponse(status_code=400, content={"message": "Bot have no rights to send messages to this chat"})
    return JSONResponse(status_code=200, content="")


@router.post("/sentry/webhook/")
async def sentry_webhook(
    request: Request,
    sentry_update: dict,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    bot_app = cast(Bot, request.state.bot_app)
    handler = await SentryHandlerFactory(db=db, bot=bot_app, update=sentry_update).get_handler()
    background_tasks.add_task(handler.handle)
    return {}
