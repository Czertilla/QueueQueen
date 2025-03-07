from utils.abstract.enum import AEnum
from aiogram.enums import ParseMode

class DBManagerType(str, AEnum):
    sqlite = "sqlite"
    postgres = "postgres"

    __default__ = sqlite


class BotParserType(AEnum, ParseMode):
    __default__ = ParseMode.HTML
