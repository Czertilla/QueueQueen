from functools import lru_cache
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from os import environ
from dotenv import load_dotenv

from utils.enums.settings import DBManagerType, TgBotFeedType
from aiogram.enums import ParseMode

load_dotenv()


class Settings(BaseSettings):
    """
    Application settings class.

    This class loads settings from environment variables and the .env file.
    It is used to manage application configuration parameters.
    """

    APP_NAME: str = "FASAPI APP"
    """Name of the FastAPI application that will be displayed in places such as Swagger."""

    DB_DBMS: DBManagerType = DBManagerType.__default__
    """Type of database management system used (e.g., sqlite, postgres)."""

    DB_NAME: str
    """Name of the database used."""

    DB_USER: str | None = None
    """Username for connecting to the database (required for PostgreSQL)."""

    DB_PASS: str | None = None
    """Password for the database user (required for PostgreSQL)."""

    DB_HOST: str | None = None
    """Hostname or IP address of the database server (required for PostgreSQL)."""

    DB_PORT: str | None = None
    """Port number on which the database server is running (required for PostgreSQL)."""

    TTL_SECONDS: int = 300
    """Time-to-live (TTL) for cache storage, in seconds."""

    BOT_TG_TOKEN: str
    """Telegram bot token issued by BotFather.
    
    For more information, visit: https://core.telegram.org/bots
    """

    BOT_TG_WEBHOOK: str
    """The HTTPS address of your application (WITHOUT THE REQUEST PATH) that Telegram will use for the webhook."""

    BOT_PARSE_MODE: ParseMode = ParseMode.HTML
    """The message parsing mode for the Telegram bot (e.g., Markdown, HTML)."""

    BOT_TG_FEED_TYPE: TgBotFeedType = TgBotFeedType.__default__

    VERSION: str
    """The version of this project, displays in messages and descripions"""

    DEV_ID_LIST: list[int] = []
    """The list of telegram ids of developers team"""

    model_config = SettingsConfigDict(env_file=environ, extra="ignore")
    """Configuration for Pydantic settings, defining how environment variables are loaded."""

    @field_validator("DB_USER", "DB_PASS", "DB_HOST", "DB_PORT", mode="before")
    @classmethod
    def check_postgres_fields(
        cls, value: str | None, info: ValidationInfo
    ) -> str | None:
        """
        Ensures that PostgreSQL-related fields are set when DB_DBMS is 'postgres'.

        Raises:
            ValueError: If a required PostgreSQL field is missing.
        """
        if info.data.get("DB_DBMS") == DBManagerType.postgres and not value:
            raise ValueError(
                f"{info.field_name} is required when DB_DBMS is set to 'postgres'")
        return value


@lru_cache
def getSettings() -> Settings:
    """
    Returns a cached instance of the application settings.

    This function ensures that the settings are only loaded once and then reused.

    Returns:
        Settings: The application settings instance.
    """
    return Settings()
