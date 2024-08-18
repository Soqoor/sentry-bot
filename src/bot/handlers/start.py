from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from sqlalchemy.ext.asyncio import AsyncSession

from src.chats.services import ChatService
from src.sentry.services import SentryService

start_router = Router()


@start_router.message(Command("start", "help"))
async def start_command_handler(message: types.Message, db: AsyncSession, command: CommandObject) -> None:
    chat_db = await ChatService(db).get_by_chat_id(chat_id=message.chat.id)
    start_message = (
        "Hi. I will help you set up alert notifications from the service https://sentry.io"
        "\n\nYou can configure notifications from the bot by installing the application "
        "to your server and creating an alert using your personal key."
        "\nOr, you can add the bot to a group chat to receive notifications together with your team."
        f"\n\nYour personal key: <code>{chat_db.chat_slug}</code>"
    )
    await message.answer(start_message)

    if command.command == "start" and command.args:
        installation = await SentryService(db).get_by_installation_id(command.args)
        if installation:
            installation.owner_id = chat_db.id
            await db.commit()
