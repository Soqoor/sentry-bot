from typing import cast

from aiogram import Bot, Dispatcher
from fastapi import APIRouter, BackgroundTasks, Depends, Request

from src.bot.dependencies import verify_secret_key

router = APIRouter()


@router.post("/telegram/", dependencies=[Depends(verify_secret_key)])
async def bot_webhook(
    request: Request,
    update_dict: dict,
    background_tasks: BackgroundTasks,
):
    bot_app = cast(Bot, request.state.bot_app)
    bot_dp = cast(Dispatcher, request.state.bot_dp)
    background_tasks.add_task(bot_dp.feed_raw_update, bot_app, update_dict)
    return {}
