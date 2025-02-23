from aiogram.types import Update
from fastapi import APIRouter
from fastapi.requests import Request
from utils.settings import Settings
from bot import bot, dp
settings = Settings()


router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
