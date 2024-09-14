from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions

from src.bot.handlers.start import start_router
from src.bot.middlewares import DBSessionMiddleware, LogUserActivityMiddleware
from src.config import settings

bot_app = Bot(
    token=settings.TG_BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        link_preview=LinkPreviewOptions(is_disabled=True),
    ),
)
bot_dp = Dispatcher()

bot_dp.message.middleware(LogUserActivityMiddleware())
bot_dp.message.middleware(DBSessionMiddleware())
bot_dp.my_chat_member.middleware(LogUserActivityMiddleware())
bot_dp.my_chat_member.middleware(DBSessionMiddleware())

bot_dp.include_routers(
    start_router,
)
