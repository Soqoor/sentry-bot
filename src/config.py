from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DOMAIN: str
    TELEGRAM_TOKEN: str
    SECRET_TOKEN: str
    DATABASE_URL: str = "sqlite:///db.sqlite3"


settings = Settings()
