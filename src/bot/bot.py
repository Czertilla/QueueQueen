from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from utils.settings import getSettings

# from .middlewares import register_middlewares
from .routers import register_routers

"""
This module initializes and configures the Aiogram bot and dispatcher.

It retrieves settings from the `getSettings()` function, creates a `Bot` 
instance with the specified token and parse mode, and initializes a 
`Dispatcher` with in-memory storage.

Routers are then registered using the `register_routers()` function.
Middleware registration is commented out but can be enabled if needed.

The resulting `bot` and `dp` objects are the main instances used for bot
operation.
"""

settings = getSettings()
bot = Bot(
    token=settings.BOT_TG_TOKEN,
    default=DefaultBotProperties(parse_mode=settings.BOT_PARSE_MODE),
)
dp = Dispatcher(storage=MemoryStorage())

# register_middlewares(dp)
register_routers(dp)
