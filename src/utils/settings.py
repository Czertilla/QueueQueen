from functools import lru_cache
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from os import environ
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "FASAPI APP"
    
   
    DB_DBMS: str = "sqlite"
    DB_NAME: str

    ADMIN_EMAIL: EmailStr
    ADMIN_EMAIL_USERNAME: str
    ADMIN_EMAIL_PASSWORD: str
    MAIL_PORT: int = 465
    MAIL_SERVER: str

    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str

    BOT_TG_TOKEN: str
    BOT_TG_WEBHOOK: str
    NOTIFIER_TG_TOKEN: str = None
    NOTIFIER_TG_CHAT: str = None

    model_config = SettingsConfigDict(env_file=environ, extra="ignore")




@lru_cache
def getSettings():
    return Settings()