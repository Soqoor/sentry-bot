from typing import cast

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from telegram import Update
from telegram.ext import Application

from src.bot.auth import verify_secret_key

router = APIRouter()


@router.post("/bot/", dependencies=[Depends(verify_secret_key)])
async def bot_webhook(
    request: Request,
    update_dict: dict,
    background_tasks: BackgroundTasks,
):
    bot_app = cast(Application, request.state.bot_app)
    update = Update.de_json(data=update_dict, bot=bot_app.bot)
    background_tasks.add_task(bot_app.process_update, update)
    return {}
