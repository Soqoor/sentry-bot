from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # base
    LOCAL_DEVELOPMENT: bool = False
    DOMAIN: str
    DATABASE_URL: str = "sqlite+aiosqlite:///database.db"

    # admin panel
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ADMIN_SECRET: str
    ADMIN_SESSION_DURATION: int = 1 * 24 * 60 * 60

    # telegram
    TG_BOT_TOKEN: str
    TG_SECRET_TOKEN: str
    TG_BOT_NAME: str

    # sentry application
    SENTRY_CLIENT_ID: str
    SENTRY_CLIENT_SECRET: str

    # sentry logging
    SENTRY_ENABLED: bool = False
    SENTRY_ENV: str = "Local"
    SENTRY_DNS: str = ""


settings = Settings()
