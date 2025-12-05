from datetime import datetime

from sqlalchemy import (DateTime, Integer, String, Text, BigInteger, ForeignKey)
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column, relationship)

class Base(DeclarativeBase):
  pass

class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
  tg_id: Mapped[int] = mapped_column(BigInteger, unique = True, index = True)
  username: Mapped[str | None] = mapped_column(String(255), nullable = True)
  created_at: Mapped[datetime] = mapped_column(DateTime, default = datetime.utcnow)
  notes: Mapped[list["Note"]] = relationship("Note", back_populates = "user", cascade = "all, delete-orphan")

class Note(Base):
  __tablename__ = "notes"

  id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
  user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), index = True)
  text: Mapped[str] = mapped_column(Text)
  created_at: Mapped[datetime] = mapped_column(DateTime, default = datetime.utcnow)
  user: Mapped[User] = relationship("User", back_populates = "notes")
