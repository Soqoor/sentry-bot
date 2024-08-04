from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from src.bot.auth import verify_secret_key
from src.bot.services import BotService
from src.database import get_db

router = APIRouter()


@router.post("/bot/", dependencies=[Depends(verify_secret_key)])
def bot_webhook(
    update_dict: dict, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    background_tasks.add_task(BotService(db=db, update_dict=update_dict).handle_update)
    return {}
