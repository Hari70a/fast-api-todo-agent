from datetime import datetime

from sqlalchemy import Column, Integer, String, JSON, func, DateTime, ForeignKey

from database.db_engine import Base


class Conversations(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    chat_id = Column(String, unique=True, index=True)
    history = Column(JSON)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default= func.now())
