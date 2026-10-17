from sqlalchemy import Column, String, Integer, Boolean

from database.db_engine import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    role = Column(String)
    is_active = Column(Boolean)
    phone_number = Column(String)

