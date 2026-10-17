from google.genai import types

from database.db_models.conversations import Conversations


def load_history(db, chat_id: str, user_id: str):
    row = db.query(Conversations).filter(
        Conversations.chat_id == chat_id,
        Conversations.user_id == user_id,
    ).first()
    if row is None:
        return None
    # Convert the stored JSON history back into types.Content objects so that GenAI SDK can use it for chat history.
    return [types.Content.model_validate(c) for c in row.history]

def save_history(db, chat_id: str, user_id: str, history: list):
    # Convert the types.Content objects into JSON-serializable format for storage.
    serialized = [content.model_dump(mode="json") for content in history]
    row = db.query(Conversations).filter(Conversations.chat_id == chat_id).first()
    if row is None:
        row = Conversations(chat_id=chat_id, user_id=user_id, history=serialized)
        db.add(row)
    else:
        row.history = serialized
    db.commit()