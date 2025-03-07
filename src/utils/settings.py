from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from os import environ
from dotenv import load_dotenv

from utils.enums.settings import BotParserType, DBManagerType

load_dotenv()

class Settings(BaseSettings):
    """
    Application settings class.

    This class loads settings from environment variables and the .env file.
    It is used to manage application configuration parameters.
    """

    APP_NAME: str = "FASAPI APP"
    """Name of the FastAPI application that will be displayed in places such as Swagger."""

    DB_DBMS: DBManagerType
    """Type of database management system used (e.g., sqlite, postgres)."""

    DB_NAME: str
    """Name of the database used."""

    if DB_DBMS == DBManagerType.postgres:
        DB_USER: str
        """Username for connecting to the database."""
        
        DB_PASS: str
        """Password for the database user."""

        DB_HOST: str
        """Hostname or IP address of the database server."""

        DB_PORT: str
        """Port number on which the database server is running."""

    TTL_SECONDS: int = 300
    """Time-to-live (TTL) for cache storage, in seconds."""

    BOT_TG_TOKEN: str
    """Telegram bot token issued by BotFather.
    
    For more information, visit: https://core.telegram.org/bots
    """

    BOT_TG_WEBHOOK: str
    """The HTTPS address of your application (WITHOUT THE REQUEST PATH) that Telegram will use for the webhook."""

    BOT_PARSE_MODE: BotParserType
    """The message parsing mode for the Telegram bot (e.g., Markdown, HTML)."""

    model_config = SettingsConfigDict(env_file=environ, extra="ignore")
    """Configuration for Pydantic settings, defining how environment variables are loaded."""


@lru_cache
def getSettings() -> Settings:
    """
    Returns a cached instance of the application settings.

    This function ensures that the settings are only loaded once and then reused.

    Returns:
        Settings: The application settings instance.
    """
    return Settings()
