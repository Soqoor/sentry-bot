from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from src.config import settings

api_key_header = APIKeyHeader(
    name="X-Telegram-Bot-Api-Secret-Token",
    auto_error=False,
)


def verify_secret_key(api_key: Optional[str] = Depends(api_key_header)):
    if api_key is None or api_key != settings.SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
