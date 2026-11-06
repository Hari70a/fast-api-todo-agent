from learn_embeddings.database.db_engine import SessionLocal
from learn_embeddings.database.save_memory import save_memory
from learn_embeddings.database.search_memories import search_memories
from learn_embeddings.utils.generate_answer import generate_answer
from learn_embeddings.utils.rerank import rerank
# from learn_embeddings.utils.get_cosine_similarity import get_cosine_similarity
# from learn_embeddings.utils.generate_embedding import generate_embedding
from learn_embeddings.utils.get_embedding import get_embedding

# texts = [
#     "I am building a FastAPI Todo Agent",
#     "I work with Python backend development",
#     "I like dosa",
#     "I use PostgreSQL for my database"
# ]


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# save_memory(
#     SessionLocal(),
#     "hariraj",
#     "I work with Python backend development"
# )

db= SessionLocal()
# save_memory(
#     db,
#     "hariraj",
#     "I use PostgreSQL for my database"
# )
# save_memory(
#     db,
#     "hariraj",
#     "I am building a FastAPI Todo Agent"
# )
#
# save_memory(
#     db,
#     "hariraj",
#     "I like dosa"
# )

# memory_embeddings = generate_embedding(texts)

query = input("What would you like to search?: ")

query_vector = get_embedding(query)

# print(len(get_embedding("Hello")), "Query vectors &&&&&&&&")

# Calculate cosine similarity for query vector with all text vectors
# results = []
# for memory in memory_embeddings:
#     similarity = get_cosine_similarity(
#         query_vector,
#         memory["embedding"]
#     )
#     results.append({
#         "text": memory["text"],
#         "score": similarity
#     })

# Search memories from db does the cosine similarity and return results
results = search_memories(
    db,
"hariraj",
    query,
    5)



# Highest similarity first(sorted already in db while using pgvector)
# results.sort(
#     key=lambda x: x["score"],
#     reverse=True
# )


# Take only the top k candidates
TOP_K = 5
top_results = results[:TOP_K]
# for out in top_results:
#     print(f"{out["score"]:.4f}",
#         out["text"])


# Set the threshold to remove the weak candidates from top_k
THRESHOLD = 0.60
candidates = [
    res
    for res in top_results
    if res["score"] >= THRESHOLD
]

# print(candidates, "Optional score threshold / reranking")

final_answers = rerank(query, candidates)

answer = generate_answer(
    query,
    final_answers
)

print(answer)