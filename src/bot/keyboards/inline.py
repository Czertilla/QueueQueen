from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.messages.messages import MessageTextBuilder
from utils.enums.callbacks import CallbackPrefix
from utils.enums.locales import LocaleKey


class InlineBuilder(InlineKeyboardBuilder):
    def __init__(self, text_builder: MessageTextBuilder, *args, **kwargs):
        """_summary_

        Args:
            text_builder (MessageTextBuilder): _description_
        """
        super().__init__(*args, **kwargs)
        self.text_builder = text_builder

    async def quit_kb(self, chat_id: int):
        """_summary_

        Args:
            chat_id (int): _description_

        Returns:
            _type_: _description_
        """
        buttons = [
            [
                InlineKeyboardButton(
                    text=await self.text_builder.get_phrase(
                        LocaleKey.quit_button
                    ),
                    callback_data=f"{CallbackPrefix.quit.value}{chat_id}"
                )
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    async def kick_kb(self, target_id: int):
        """_summary_

        Args:
            target_id (int): _description_
        """
        buttons = [
            [
                InlineKeyboardButton(
                    text=await self.text_builder.get_phrase(
                        LocaleKey.cansel_button
                    ),
                    callback_data=CallbackPrefix.cansel.value
                ),
                InlineKeyboardButton(
                    text=await self.text_builder.get_phrase(
                        LocaleKey.kick_button
                    ),
                    callback_data=f"{CallbackPrefix.kick.value}{target_id}"
                )
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
