import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import AsyncEngine

from app.config import settings
from app.database import engine
from app.models import Base
from app.handlers import start, notes

logging.basicConfig(level = logging.INFO, format = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

async def init_db(engine_: AsyncEngine):
  async with engine_.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

  logger.info("Database tables initialized")

async def main():
  if not settings.bot_token:
    raise RuntimeError("BOT_TOKEN is not set")

  await init_db(engine)

  bot = Bot(token = settings.bot_token, default = DefaultBotProperties(parse_mode = "HTML"))
  dp = Dispatcher(storage = MemoryStorage())

  dp.include_router(start.router)
  dp.include_router(notes.router)

  logger.info("Bot started")
  await dp.start_polling(bot)

if __name__ == "__main__":
  try:
    asyncio.run(main())
  except (KeyboardInterrupt, SystemExit):
    logger.info("Bot stopped")
