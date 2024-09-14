from aiogram import Router, types
from aiogram.enums import ChatType
from aiogram.filters import JOIN_TRANSITION, LEAVE_TRANSITION, ChatMemberUpdatedFilter, Command, CommandObject
from aiogram.types import ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession

from src.chats.services import ChatService
from src.sentry.services import SentryService

start_router = Router()

wellcome_message = (
    'Hi! I’ll help you set up alert notifications from <a href="https://sentry.io/">Sentry.io</a>\n\n'
    'To get started, install the "Telegram Alerts Bot" from the Sentry integrations library on your Sentry server,'
    " and create an alert using your personal key.\n"
    "You can use the key below to receive notifications in this chat,"
    " or add the bot to another chat or group to get a key there.\n\n"
    "Your personal key: <code>{}</code>"
)


@start_router.message(Command("start", "help"))
async def start_command_handler(message: types.Message, db: AsyncSession, command: CommandObject) -> None:
    chat_db = await ChatService(db).get_by_chat_id(chat_id=message.chat.id)
    await message.answer(wellcome_message.format(chat_db.chat_slug))

    if command.command == "start" and command.args:
        installation = await SentryService(db).get_by_installation_id(command.args)
        if installation:
            installation.owner_id = chat_db.id
            await db.commit()


@start_router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def join_chat_handler(event: ChatMemberUpdated, db: AsyncSession) -> None:
    if event.chat.type != ChatType.PRIVATE:
        chat_db = await ChatService(db).get_by_chat_id(chat_id=event.chat.id)
        await event.bot.send_message(chat_id=event.chat.id, text=wellcome_message.format(chat_db.chat_slug))


@start_router.my_chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
async def leave_chat_handler(event: ChatMemberUpdated, db: AsyncSession) -> None:
    chat_db = await ChatService(db).get_by_chat_id(chat_id=event.chat.id)
    chat_db.is_active = False
    await db.commit()
