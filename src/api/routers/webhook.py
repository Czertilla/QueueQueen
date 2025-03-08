from aiogram.types import Update
from fastapi import APIRouter
from fastapi.requests import Request

from bot import bot, dp
from utils.settings import Settings

settings = Settings()

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("")
async def webhook(request: Request) -> None:
    """
    Handles incoming Telegram updates via webhook.

    Validates the request JSON as an aiogram Update model and feeds it
    to the aiogram Dispatcher.

    Args:
        request: The FastAPI Request object containing the update data.
    """
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
