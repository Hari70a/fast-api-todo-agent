from LLM.build_memory_context import build_memory_context


def build_message_with_memory(
    question: str,
    memories: list[dict],
) -> str:

    memory_context = build_memory_context(memories)

    if not memory_context:
        return question

    return f"""
        {memory_context}
        
        Current user message:
        {question}
        """.strip()