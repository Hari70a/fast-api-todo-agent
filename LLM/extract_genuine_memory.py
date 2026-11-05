# utils/extract_memories.py

from google import genai
from google.genai import types
from pydantic import BaseModel, Field


class ExtractedMemory(BaseModel):
    text: str = Field(
        description="A concise durable fact or preference about the user"
    )
    memory_type: str = Field(
        description=(
            "One of: preference, project, technical_context, personal_fact"
        )
    )


class MemoryExtractionResult(BaseModel):
    memories: list[ExtractedMemory]


def extract_genuine_memories(
    client: genai.Client,
    model: str,
    user_message: str,
) -> list[ExtractedMemory]:

    prompt = f"""
        Extract durable facts or preferences about the user from the message below.
        
        Store only information that could be useful in a future conversation.
        
        Good examples:
        - User prefers concise Python examples.
        - User is building a FastAPI Todo Agent.
        - User uses PostgreSQL.
        - User is learning semantic memory retrieval.
        
        Do not store:
        - Greetings or thanks.
        - Temporary questions.
        - Todo commands such as create, delete or complete a task.
        - Passwords, access tokens, API keys or authentication data.
        - Tool output.
        - Facts invented by the assistant.
        - Information that is not explicitly stated by the user.
        
        If nothing should be remembered, return an empty memories array.
        
        User message:
        {user_message}
        """.strip()

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MemoryExtractionResult,
            temperature=0,
        ),
    )

    result = response.parsed

    if not result:
        return []

    return result.memories