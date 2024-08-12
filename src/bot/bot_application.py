from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler

from src.bot.handlers.message import message_handler
from src.bot.handlers.start import start_handler
from src.config import settings


async def get_bot_application():
    application = ApplicationBuilder().token(settings.TG_BOT_TOKEN).build()

    application.add_handler(CommandHandler(command="start", callback=start_handler))
    application.add_handler(MessageHandler(filters=None, callback=message_handler))

    await application.initialize()

    print("=" * 20)
    print("=" * 20)
    print("=" * 20)
    print("BOT APPLICATION LOADED")
    print("=" * 20)
    print("=" * 20)
    print("=" * 20)

    return application
