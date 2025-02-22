from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from src.utils.settings import getSettings
# from .middlewares import register_middlewares
from .routers import register_routers

settings = getSettings()
bot = Bot(token=settings.BOT_TG_TOKEN, default=DefaultBotProperties(parse_mode=settings.BOT_PARSE_MODE))
dp = Dispatcher(storage=MemoryStorage())

# register_middlewares(dp)
register_routers(dp)
