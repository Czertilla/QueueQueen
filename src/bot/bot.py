from utils.mixins.singleton import SingletonMixin
from aiogram import Bot as Base, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from utils.settings import Settings


class Bot(Base, SingletonMixin):
    def __init__(self):
        super().__init__(token=Settings().BOT_TG_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dp = Dispatcher()