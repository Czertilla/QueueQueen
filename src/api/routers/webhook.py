import logging
from aiogram import Dispatcher

from aiogram.types import Message, Update, ChatMemberAdministrator
from aiogram.filters import CommandStart
from fastapi import APIRouter
from fastapi.requests import Request

from services.queues import QueueService
from services.users import UserService
from utils.settings import Settings
from api.dependencies import AllUOW
from bot import bot
settings = Settings()

dp = bot.dp

router = APIRouter(prefix="/webhook", tags=["webhook"])

@dp.message(CommandStart())
async def start(message: Message) -> None:
    user = message.from_user
    await UserService(uow := AllUOW()).check_user(user)
    member = message.chat.get_member(user.id)
    if isinstance(member, ChatMemberAdministrator):
        QueueService(uow).check_chat()  


@router.post("")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
