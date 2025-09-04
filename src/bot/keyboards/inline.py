from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.messages.messages import MessageTextBuilder
from utils.enums.callbacks import CallbackPrefix
from utils.enums.locales import LocaleKey


class InlineBuilder(InlineKeyboardBuilder):
    def __init__(self, text_builder: MessageTextBuilder, *args, **kwargs):
        """
        Custom inline keyboard builder with localization support.

        Args:
            text_builder (MessageTextBuilder): An instance for getting
            localized phrases.
        """
        super().__init__(*args, **kwargs)
        self.text_builder = text_builder

    async def quit_kb(self, chat_id: int) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard with a button to exit the chat.

        Args:
            chat_id (int): The chat ID.

        Returns:
            InlineKeyboardMarkup: An inline keyboard object.
        """
        buttons = [
            [
                InlineKeyboardButton(
                    text=await self.text_builder.get_phrase(
                        LocaleKey.quit_button
                    ),
                    callback_data=f"{CallbackPrefix.quit.value}{chat_id}",
                )
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    async def kick_kb(self, target_id: int) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard to confirm the user's kick.

        Args:
            target_id (int): The ID of the user to kick.

        Returns:
            InlineKeyboardMarkup: An inline keyboard object with undo and
            kick buttons.
        """
        buttons = [
            [
                InlineKeyboardButton(
                    text=await self.text_builder.get_phrase(
                        LocaleKey.cansel_button
                    ),
                    callback_data=CallbackPrefix.cansel.value,
                ),
                InlineKeyboardButton(
                    text=await self.text_builder.get_phrase(
                        LocaleKey.kick_button
                    ),
                    callback_data=f"{CallbackPrefix.kick.value}{target_id}",
                ),
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    async def queue_kb(self) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(
                    text=await self.text_builder.get_phrase(
                        LocaleKey.join_button
                    ),
                    callback_data="queue/join",
                ),
                InlineKeyboardButton(
                    text=await self.text_builder.get_phrase(
                        LocaleKey.quit_button
                    ),
                    callback_data="queue/quit",
                ),
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    async def invite_kb(self, bot_username: str) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard to invite bot to chat.

        Args:
            bot_username (str): bot username to put it in callback link

        Returns:
            InlineKeyboardMarkup:  An inline keyboard object with invite button.
        """
        buttons = [
            [
                InlineKeyboardButton(
                    text=await self.text_builder.get_phrase(
                        LocaleKey.invite_button
                    ),
                    url=f"https://t.me/{bot_username}?startgroup=start",
                )
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
