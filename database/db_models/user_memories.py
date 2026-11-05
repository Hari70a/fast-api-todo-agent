from sqlalchemy import Column, Integer, String, DateTime, func, Text, ForeignKey
from pgvector.sqlalchemy import VECTOR

from database.db_engine import Base


class UserMemories(Base):
    __tablename__ = "user_memories"

    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        index=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    memory_text = Column(
        Text,
        nullable=False
    )
    embedding = Column(
        VECTOR(3072),
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    memory_type = Column(
        String(30),
        nullable=True
    )
