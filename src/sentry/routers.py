from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.chats.services import ChatService
from src.config import settings
from src.database import get_db
from src.sentry.services import SentryService

router = APIRouter()


@router.get("/sentry/install/")
async def install_endpoint(code: str, installationId: str, orgSlug: str, db: AsyncSession = Depends(get_db)):
    await SentryService(db=db).new_installation(
        installation_id=installationId,
        code=code,
        org_slug=orgSlug,
    )
    return RedirectResponse(f"https://t.me/{settings.TG_BOT_NAME}?start={installationId}")


@router.post("/sentry/alert-rule")
async def alert_rule_endpoint(update_dict: dict, db: AsyncSession = Depends(get_db)):
    chat_slug = update_dict.get("fields")[0].get("value")
    error_message = await ChatService(db).check_chat_slug(chat_slug)
    if error_message:
        return JSONResponse(status_code=400, content={"message": error_message})
    return JSONResponse(status_code=200, content="")


@router.post("/sentry/webhook/")
async def sentry_webhook(
    sentry_alert_dict: dict,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    background_tasks.add_task(SentryService(db=db, sentry_alert_dict=sentry_alert_dict).handle_sentry_alert)
    return {}
