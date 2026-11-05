from LLM.client import client

def get_embedding(text: str):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values