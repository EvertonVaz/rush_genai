from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from chatbot.models import Message, Base, PrePrompt, Summary
from chatbot.schemas import MessageData, SummaryData

DATABASE_URL = "sqlite:///./chat_history.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class MessageRepository:
    def __init__(self, db_session=None):
        self.db_session = db_session if db_session else next(get_db())

    def add_message(self, role: str, content: str) -> Message:
        message = Message(role=role, content=content)
        self.db_session.add(message)
        self.db_session.commit()
        self.db_session.refresh(message)
        return message

    def add_summary(self, content: str) -> Summary:
        summary = Summary(content=content)
        self.db_session.add(summary)
        self.db_session.commit()
        self.db_session.refresh(summary)
        return summary

    def get_last_n_messages(self, n: int) -> list[MessageData]:
        messages = (
            self.db_session.query(Message)
            .order_by(Message.created_at.desc())
            .limit(n)
            .all()
        )

        result = []
        for msg in messages:
            result.append(MessageData(role=msg.role, content=msg.content))
        return result

    def get_total_messages_count(self) -> int:
        count = self.db_session.query(Message).count()
        return count

    def get_lasts_summary(self) -> list[SummaryData]:
        summarys = (
            self.db_session.query(Summary)
            .order_by(Summary.created_at.desc())
            .limit(10)
            .all()
        )
        result = []
        for summary in summarys:
            result.append(SummaryData(content=summary.content))
        return result

    def add_preprompt(self, content: str):
        preprompt = PrePrompt(content=content)
        self.db_session.add(preprompt)
        self.db_session.commit()
        self.db_session.refresh(preprompt)
        return preprompt