
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from database.db_engine import Base


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    description = Column(String)
    complete = Column(Boolean)
    priority = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))