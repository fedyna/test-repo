from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_env: str = Field(default="dev", alias="APP_ENV")
    database_url: str = Field(alias="DATABASE_URL")
    redis_url: str = Field(alias="REDIS_URL")
    basic_auth_user: str = Field(default="admin", alias="BASIC_AUTH_USER")
    basic_auth_password: str = Field(default="admin", alias="BASIC_AUTH_PASSWORD")
    youtube_api_key: str | None = Field(default=None, alias="YOUTUBE_API_KEY")
    telegram_bot_token: str | None = Field(default=None, alias="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: str | None = Field(default=None, alias="TELEGRAM_CHAT_ID")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
