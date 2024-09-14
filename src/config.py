from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # base
    LOCAL_DEVELOPMENT: bool = False
    DOMAIN: str

    # postgres database
    DB_NAME: str = ""
    DB_HOST: str = ""
    DB_PORT: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""

    # admin panel
    ADMIN_USERNAME: str = ""
    ADMIN_PASSWORD: str = ""
    ADMIN_SECRET: str = ""
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

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        if self.DB_NAME:
            return (
                f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        return "sqlite+aiosqlite:///database.db"


settings = Settings()
