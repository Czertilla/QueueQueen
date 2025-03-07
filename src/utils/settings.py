from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from os import environ
from dotenv import load_dotenv
from aiogram.enums import ParseMode

load_dotenv()

class Settings(BaseSettings):
    """
    Application settings class.

    Loads settings from environment variables and .env file.
    """

    APP_NAME: str = "FASAPI APP"
    """Name of the FastAPI application that will be displayed in places such as Swagger."""

    DB_DBMS: str = "sqlite"
    """Type of database management system used (e.g., sqlite, postgres)."""
    DB_NAME: str
    """Name of database used."""

    TTL_SECONDS: int = 300
    """TTL cache storage time in seconds."""

    BOT_TG_TOKEN: str
    """Token of the Telegram bot, which is issued by BotFather.
    For more information, visit https://core.telegram.org/bots."""
    BOT_TG_WEBHOOK: str
    """The HTTPS address of your application (WITHOUT THE REQUEST PATH) that Telegram for webhook will use."""
    BOT_PARSE_MODE: ParseMode = ParseMode.HTML
    """"""

    model_config = SettingsConfigDict(env_file=environ, extra="ignore")


@lru_cache
def getSettings() -> Settings:
    """
    Returns a cached instance of the application settings.

    Returns:
        Settings: The application settings instance.
    """
    return Settings()