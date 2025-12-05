from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker, AsyncSession)
from app.config import settings

if not settings.database_url:
  raise RuntimeError("DATABASE_URL is not set")

engine = create_async_engine(settings.database_url, echo = False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit = False, class_ = AsyncSession)

async def get_session() -> AsyncSession:
  return AsyncSessionLocal()
