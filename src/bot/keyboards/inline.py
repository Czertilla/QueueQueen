from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.messages.messages import MessageTextBuilder
from utils.enums.callbacks import CallbackPrefix
from utils.enums.locales import LocaleKey


class InlineBuilder(InlineKeyboardBuilder):
    def __init__(self, text_builder: MessageTextBuilder, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_builder = text_builder

    async def quit_kb(self, chat_id: int):
        buttons = [
            [
                InlineKeyboardButton(
                    text=await self.text_builder.get_phrase(
                        LocaleKey.quit_button
                    ),
                    callback_data=f"{CallbackPrefix.quit}{chat_id}"
                )
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
