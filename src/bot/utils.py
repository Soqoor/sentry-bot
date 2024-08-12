from telegram.ext import Application


async def async_send_message(bot_app: Application, chat_id, text):
    await bot_app.bot.send_message(
        chat_id=chat_id,
        text=text,
    )
