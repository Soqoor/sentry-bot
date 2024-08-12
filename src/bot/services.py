import httpx

from src.config import settings


async def setup_webhook():
    async with httpx.AsyncClient() as client:
        await client.get(
            f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}"
            "/setWebhook"
            f"?url=https://{settings.DOMAIN}/bot/"
            f"&secret_token={settings.TG_SECRET_TOKEN}"
        )
