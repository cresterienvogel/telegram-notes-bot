from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (Message, ReplyKeyboardMarkup, KeyboardButton)
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import User

router = Router()

def main_menu_keyboard() -> ReplyKeyboardMarkup:
  return ReplyKeyboardMarkup(
    keyboard = [
      [KeyboardButton(text = "Create note")],
      [KeyboardButton(text = "All notes")],
      [KeyboardButton(text = "Delete note")]
    ],
    resize_keyboard = True
  )

@router.message(CommandStart())
async def cmd_start(message: Message):
  tg_user = message.from_user

  async with AsyncSessionLocal() as session:
    result = await session.execute(select(User).where(User.tg_id == tg_user.id))
    user = result.scalar_one_or_none()

    if user is None:
      user = User(tg_id = tg_user.id, username = tg_user.username)
      session.add(user)
      await session.commit()

      text = (
        f"Hi, <b>{tg_user.first_name}</b>!\n\n"
        "Use the buttons below to work with notes"
      )
    else:
      text = (
        f"Welcome back, <b>{tg_user.first_name}</b>!\n"
        "Use the buttons below to work with notes"
      )

  await message.answer(text, reply_markup = main_menu_keyboard())
