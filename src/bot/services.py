import requests
from sqlalchemy.orm import Session
from telegram import Update

from src.config import settings
from src.users import schemas
from src.users.services import ChatService


class BotService:
    api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}"

    def __init__(self, db: Session, update_dict: dict):
        self.db = db
        self.update_dict = update_dict

    @classmethod
    def setup_webhook(cls):
        requests.get(
            cls.api_url
            + (
                "/setWebhook"
                f"?url=https://{settings.DOMAIN}/bot/"
                f"&secret_token={settings.SECRET_TOKEN}"
            ),
            timeout=20,
        )

    def handle_update(self):
        update = Update.de_json(data=self.update_dict)
        chat = schemas.CreateOrUpdateChat(
            chat_id=update.effective_chat.id,
            chat_type=update.effective_chat.type,
            username=update.effective_user.username or "",
            first_name=update.effective_user.first_name or "",
            last_name=update.effective_user.last_name or "",
            chat_title=update.effective_chat.title or "",
            chat_inviter=update.effective_user.id,
        )
        ChatService.create_or_update(db=self.db, chat=chat)
