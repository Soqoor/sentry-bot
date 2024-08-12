from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Update
from telegram.ext import CallbackContext

from src.bot.dependencies import with_db_session
from src.bot.utils import async_send_message


@with_db_session
async def start_handler(update: Update, context: CallbackContext, db: AsyncSession):
    await async_send_message(
        bot_app=context.bot,
        chat_id=update.effective_chat.id,
        text=f"Start Echo: {update.effective_message.text=}",
    )
