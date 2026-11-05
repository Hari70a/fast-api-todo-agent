from fastapi import Depends
from sqlalchemy.orm import Session

from database.db_models.user_memories import UserMemories
# from database.db_utils.db_dependency import db_dependency
from utils.get_embedding import get_embedding


def save_memory(
    db:Session,
    user_id: int,
    text: str,
    memory_type: str = "fact"
):
    cleaned_text = text.strip()

    if not cleaned_text:
        return None

    existing_memory = (
        db.query(UserMemories)
        .filter(
            UserMemories.user_id == user_id,
            UserMemories.memory_text == cleaned_text,
        )
        .first()
    )

    if existing_memory:
        return existing_memory

    print(db, "db: db_dependency,")
    embedding = get_embedding(text)

    memory = UserMemories(
        user_id=user_id,
        memory_text=text,
        embedding=embedding,
        memory_type=memory_type,
    )

    try:
        db.add(memory)
        db.commit()
        db.refresh(memory)
        return memory

    except Exception:
        db.rollback()
        raise