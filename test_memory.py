import os

from dotenv import load_dotenv
from mem0 import Memory

load_dotenv()

# print(os.environ["GEMINI_API_KEY"], "GOOGLE API KEY @@@@@@@")
GOOGLE_API_KEY = os.environ["GEMINI_API_KEY"]

config = {
    "llm": {
        "provider": "gemini",
        "config": {
            "model": "gemini-flash-lite-latest",
            "api_key": GOOGLE_API_KEY,
        },
    },
    "embedder": {
        "provider": "gemini",
        "config": {
            "model": "models/gemini-embedding-001",
            "api_key": GOOGLE_API_KEY,
            "embedding_dims": 768,
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "todo_memories",
            "embedding_model_dims": 768
        }
    }
}

memory = Memory.from_config(config)

memory.add(
    "I am building a FastAPI Todo Agent",
    user_id="hariraj"
)

print("learn_embeddings added")


output = memory.search(
    query="What project am I working on?",
   filters = {
        "user_id": "hariraj"
   }
)
results = output.get("results")
memory = results[0].get("learn_embeddings")

print(memory, "learn_embeddings @@@@@@@")