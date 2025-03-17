from logging import getLogger
from aiogram import Bot, Router, F
from aiogram.types import Message, InputMediaDocument
from aiogram.filters import Command, CommandObject
from aiogram.types.input_file import FSInputFile
from re import match
from utils.enums.commands import LogFileType
import os
from utils.settings import getSettings


router = Router()
router.message.filter(F.from_user.id.in_(getSettings().DEV_ID_LIST))

logger = getLogger(__name__)


@router.message(Command("log"))
async def get_log_files(message: Message,  command: CommandObject):
    backup_count = 0
    filetype = LogFileType.log
    if command.args is not None:
        try:
            arguments = command.args.split()
            filetype = LogFileType(arguments[0])
            if len(arguments) > 1:
                backup_count = arguments[1]
        except Exception as e:
            await message.reply(f"invalid command. raised {e}")
            return
    prefix = "."+str(backup_count) if backup_count else ""
    if os.path.isfile(path := f"logs/app.{filetype.value}{prefix}"):
        answer = await message.answer("loading...")
        await answer.edit_media(
            media=InputMediaDocument(media=FSInputFile(path), caption="done"),
        )
    else:
        await message.reply("file doesn`t exist")
