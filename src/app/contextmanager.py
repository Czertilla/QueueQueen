# from redis import asyncio as aioredis
from fastapi.concurrency import asynccontextmanager
from collections.abc import AsyncIterator
from fastapi import FastAPI
import sys

from utils.settings import Settings
from bot import bot

# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
settings = Settings()


async def startup(app: FastAPI):
    # redis = aioredis.from_url("redis://localhost")
    # FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await bot.set_webhook(url=f"{settings.BOT_TG_WEBHOOK}/webhook",
                          allowed_updates=bot.dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    ...

async def shutdown(app: FastAPI):
    await bot.delete_webhook()
    ...


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await startup(app)
    yield
    await shutdown(app)
