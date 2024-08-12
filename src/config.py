from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # base
    DOMAIN: str
    DATABASE_URL: str = "sqlite+aiosqlite:///database.db"

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
