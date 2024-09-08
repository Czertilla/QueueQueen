from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

from utils.settings import Settings

settings = Settings()
engine = create_async_engine(f"sqlite+aiosqlite:///{settings.DB_NAME}.db")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

if __name__ == "__main__":
    from database.sqlalchemy.base import Base
    asyncio.run(create_tables())
