from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from os import environ
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram.enums import ParseMode

load_dotenv()   

class Settings(BaseSettings):
    APP_NAME: str = "FASAPI APP"
    """name of fastAPI application that will be displayed in places such as swagger"""
   
    DB_DBMS: str = "sqlite"
    """type of database management system used (e.g. sqlite, postgres)"""
    DB_NAME: str
    """name of database used"""

    TTL_SECONDS: int = 300
    """TTL cache storage time in seconds"""

    BOT_TG_TOKEN: str
    """токен используемого бота, который выдается BotFather.
    Для более подробной информации посетите https://core.telegram.org/bots"""
    BOT_TG_WEBHOOK: str
    """The https address of your application (WITHOUT THE REQUEST PATH) that telegram for webhook will use."""
    BOT_PARSE_MODE: str = ParseMode.HTML

    model_config = SettingsConfigDict(env_file=environ, extra="ignore")




@lru_cache
def getSettings():
    return Settings()