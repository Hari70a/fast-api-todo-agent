from sqlalchemy.orm import Session

from LLM.extract_genuine_memory import extract_genuine_memories
from database.db_utils.save_memory import save_memory


def process_memory(
    db: Session,
    client,
    model: str,
    user_id: int,
    user_message: str,
) -> list[str]:
    extracted = extract_genuine_memories(
        client=client,
        model=model,
        user_message=user_message,
    )

    saved_memories = []

    for item in extracted:
        memory = save_memory(
            db=db,
            user_id=user_id,
            text=item.text,
            memory_type=item.memory_type,
        )

        if memory:
            saved_memories.append(memory.memory_text)

    return saved_memories