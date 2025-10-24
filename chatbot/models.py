from enum import Enum
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base
from chatbot.schemas import RoleType

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[RoleType] = mapped_column(String(10), nullable=False) # 'user' or 'assistant'
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __str__(self):
        return f"{self.role}: {self.content}"

    def __repr__(self):
        return f"<Message(id={self.id}, role='{self.role}', content='{self.content[:50]}...')>"


class Summary(Base):
    __tablename__ = "summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __str__(self):
        return f"{self.summary_type}: {self.content}"

    def __repr__(self):
        return f"<Summary(id={self.id}, summary_type='{self.summary_type}', content='{self.content[:50]}...')>"


class PrePrompt(Base):
    __tablename__ = "preprompts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    def __str__(self):
        return f"PrePrompt: {self.content}"

    def __repr__(self):
        return f"<PrePrompt(id={self.id}, content='{self.content[:50]}...')>"

class UserMovies(Base):
    __tablename__ = "user_movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filme_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    rating: Mapped[float] = mapped_column(Integer, nullable=False, default=0)
    is_favorite: Mapped[bool] = mapped_column(Integer, nullable=False, default=0)
    watching: Mapped[bool] = mapped_column(Integer, nullable=False, default=0)


    def __str__(self):
        return f"User: {self.username}"

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"