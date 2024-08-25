import datetime
import secrets

from fastapi.requests import Request
from sqladmin.authentication import AuthenticationBackend

from src.config import settings

active_tokens = {}


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            token = secrets.token_hex(32)
            active_tokens[token] = datetime.datetime.now().timestamp()
            request.session.update({"token": token})
            await self.remove_old_tokens()
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        if settings.LOCAL_DEVELOPMENT:
            return True
        token = request.session.get("token")
        return token and await self.token_is_valid(token)

    @staticmethod
    async def token_is_valid(token: str) -> bool:
        token_issued = active_tokens.get(token)
        if token_issued:
            valid_until = token_issued + settings.ADMIN_SESSION_DURATION
            return datetime.datetime.now().timestamp() < valid_until
        return False

    async def remove_old_tokens(self):
        tokens_to_remove = [token for token in active_tokens if not await self.token_is_valid(token)]
        for token in tokens_to_remove:
            active_tokens.pop(token)


authentication_backend = AdminAuth(secret_key=settings.ADMIN_SECRET)


def last_activity_format(model, attribute) -> str:
    days_ago = (datetime.datetime.now() - getattr(model, attribute)).days
    if days_ago > 365:
        return f"{days_ago // 365} year"
    if days_ago > 30:
        return f"{days_ago // 30} month"
    if days_ago:
        return f"{days_ago} day"
    return "Today"
