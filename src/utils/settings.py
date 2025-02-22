from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from os import environ
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram.enums import ParseMode

load_dotenv()   

class Settings(BaseSettings):
    APP_NAME: str = "FASAPI APP"
   
    DB_DBMS: str = "sqlite"
    DB_NAME: str

    BOT_TG_TOKEN: str
    BOT_TG_WEBHOOK: str
    BOT_PARSE_MODE: str = ParseMode.HTML

    model_config = SettingsConfigDict(env_file=environ, extra="ignore")




@lru_cache
def getSettings():
    return Settings()