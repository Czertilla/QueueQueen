# from redis import asyncio as aioredis
from fastapi.concurrency import asynccontextmanager
from collections.abc import AsyncIterator
from fastapi import FastAPI

from utils.settings import Settings
from bot import bot, dp

# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
settings = Settings()


async def startup(app: FastAPI):
    """
    Asynchronous startup function for the FastAPI application.

    This function performs initialization tasks such as setting the Telegram bot
    webhook, configuring allowed updates, and potentially initializing a cache
    (commented out in the code).

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    # redis = aioredis.from_url("redis://localhost")
    # FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await bot.set_webhook(
        url=f"{settings.BOT_TG_WEBHOOK}/webhook",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    ...  # Add other startup tasks here


async def shutdown(app: FastAPI):
    """
    Asynchronous shutdown function for the FastAPI application.

    This function performs cleanup tasks such as deleting the Telegram bot 
    webhook.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    await bot.delete_webhook()
    ...  # Add other shutdown tasks here


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Asynchronous context manager for the FastAPI application's lifespan.

    This context manager encapsulates the startup and shutdown procedures of 
    the application.
    It executes the `startup` function upon entering the context and the
    `shutdown` function upon exiting.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Yields control to the application during its lifespan.
    """
    await startup(app)
    yield
    await shutdown(app)
