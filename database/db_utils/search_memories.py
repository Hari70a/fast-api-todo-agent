from database.db_models.user_memories import UserMemories
from utils.get_embedding import get_embedding


def search_memories(
        db,
        user_id: int,
        query: str,
        limit: int = 5
):
    query_embedding = get_embedding(query)
    cosine_dist = UserMemories.embedding.cosine_distance(
        query_embedding
    )

    rows = (
        db.query(
            UserMemories,
            cosine_dist.label("distance")
        )
        .filter(
            UserMemories.user_id == user_id
        )
        .order_by(cosine_dist)
        .limit(limit)
        .all()
    )

    results = []

    for memory, distance_value in rows:
        similarity = 1 - distance_value

        results.append({
            "text": memory.memory_text,
            "similarity": similarity
        })

    return results