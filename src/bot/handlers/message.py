from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Update
from telegram.ext import CallbackContext

from src.bot.dependencies import with_db_session
from src.bot.utils import async_send_message


@with_db_session
async def message_handler(update: Update, context: CallbackContext, db: AsyncSession):
    print("Handler started")
    print("Handler started")
    print("Handler started")
    await async_send_message(
        bot_app=context.bot,
        chat_id=update.effective_chat.id,
        text=f"Message Echo: {update.effective_message.text=}",
    )
