from utils.settings import Settings
from sqlalchemy.ext.asyncio import create_async_engine

settings = Settings()
pgs_url = f"{settings.DB_USER}:{
    settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_async_engine(f"postgresql+asyncpg://{pgs_url}")
