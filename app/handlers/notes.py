from sqlalchemy import select

from aiogram import Router, F
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.database import AsyncSessionLocal
from app.models import User, Note
from app.handlers.start import main_menu_keyboard

router = Router()

class NoteStates(StatesGroup):
  waiting_text = State()

def make_delete_keyboard(notes: list[Note]) -> InlineKeyboardMarkup:
  rows: list[list[InlineKeyboardButton]] = []

  for idx, n in enumerate(notes, start = 1):
    title = n.text.strip().splitlines()[0]
    if len(title) > 30:
      title = title[:27] + "..."

    label = f"{idx}. {title}"
    rows.append([InlineKeyboardButton(text = label, callback_data = f"del:{n.id}")])

  rows.append([InlineKeyboardButton(text = "Cancel", callback_data = "cancel_delete")])
  return InlineKeyboardMarkup(inline_keyboard = rows)

@router.message(F.text == "Create note")
async def add_note_start(message: Message, state: FSMContext):
  await state.set_state(NoteStates.waiting_text)
  await message.answer("Send me a note text\n\nUse /start to cancel")

@router.message(NoteStates.waiting_text)
async def add_note_save(message: Message, state: FSMContext):
  text = (message.text or "").strip()
  if not text:
    await message.answer("Note cannot be empty")
    return

  async with AsyncSessionLocal() as session:
    user_result = await session.execute(select(User).where(User.tg_id == message.from_user.id))
    user = user_result.scalar_one_or_none()

    if user is None:
      await state.clear()
      await message.answer("Send /start first", reply_markup = main_menu_keyboard())
      return

    note = Note(user_id = user.id, text = text)
    session.add(note)

    await session.commit()
    await session.refresh(note)

  await state.clear()
  await message.answer("Note has been saved", reply_markup = main_menu_keyboard())

@router.message(F.text == "All notes")
async def list_notes(message: Message):
  async with AsyncSessionLocal() as session:
    user_result = await session.execute(select(User).where(User.tg_id == message.from_user.id))
    user = user_result.scalar_one_or_none()

    if user is None:
      await message.answer("Send /start first", reply_markup = main_menu_keyboard())
      return

    notes_result = await session.execute(select(Note).where(Note.user_id == user.id).order_by(Note.created_at))
    notes = notes_result.scalars().all()

  if not notes:
    await message.answer("No notes yet", reply_markup = main_menu_keyboard())
    return

  lines = []
  for idx, n in enumerate(notes, start = 1):
    lines.append(f"{idx}. {n.text}")

  await message.answer("Your notes:\n\n" + "\n".join(lines), reply_markup = main_menu_keyboard())

@router.message(F.text == "Delete note")
async def delete_note_menu(message: Message):
  async with AsyncSessionLocal() as session:
    user_result = await session.execute(select(User).where(User.tg_id == message.from_user.id))
    user = user_result.scalar_one_or_none()

    if user is None:
      await message.answer("Send /start first", reply_markup = main_menu_keyboard())
      return

    notes_result = await session.execute(select(Note).where(Note.user_id == user.id).order_by(Note.created_at))
    notes = notes_result.scalars().all()

  if not notes:
    await message.answer("No notes yet", reply_markup = main_menu_keyboard())
    return

  kb = make_delete_keyboard(notes)
  await message.answer("Choose note to delete:", reply_markup = kb)

@router.callback_query(F.data == "cancel_delete")
async def cancel_delete(callback: CallbackQuery):
  try:
    await callback.message.edit_text("Deletion canceled")
  except Exception:
    pass

  await callback.message.answer("What's next?", reply_markup = main_menu_keyboard())
  await callback.answer()

@router.callback_query(F.data.startswith("del:"))
async def delete_note(callback: CallbackQuery):
  _, note_id_str = callback.data.split(":")
  note_id = int(note_id_str)

  async with AsyncSessionLocal() as session:
    user_result = await session.execute(select(User).where(User.tg_id == callback.from_user.id))
    user = user_result.scalar_one_or_none()

    if user is None:
      await callback.answer("Send /start first", show_alert = True)
      return

    note_result = await session.execute(select(Note).where(Note.id == note_id, Note.user_id == user.id))
    note = note_result.scalar_one_or_none()

    if note is None:
      await callback.answer("Note is not found", show_alert = True)
      return

    await session.delete(note)
    await session.commit()

  try:
    await callback.message.edit_text("Note has been deleted")
  except Exception:
    pass

  await callback.answer()
