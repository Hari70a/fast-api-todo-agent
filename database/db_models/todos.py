from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func

from database.db_engine import Base


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    description = Column(String)
    complete = Column(Boolean)
    priority = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)