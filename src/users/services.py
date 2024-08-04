import datetime

from sqlalchemy.orm import Session

from src.users import models, schemas


class ChatService:

    @staticmethod
    def create_or_update(db: Session, chat: schemas.CreateOrUpdateChat):
        db_chat = db.query(models.Chat).filter_by(chat_id=chat.chat_id).first()
        if db_chat:
            db_chat.last_activity = datetime.datetime.now()
            db_chat.user_activity_counter += 1
            db_chat.is_active = True
            db_chat.username = chat.username
            db_chat.first_name = chat.first_name
            db_chat.last_name = chat.last_name
            db_chat.chat_title = chat.chat_title
            db.commit()
        else:
            db_chat = models.Chat(**chat.dict())
            db.add(db_chat)
            db.commit()
