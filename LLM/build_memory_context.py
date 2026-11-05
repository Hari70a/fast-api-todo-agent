def build_memory_context(memories: list[dict]) -> str:
    if not memories:
        return ""

    memory_lines = "\n".join(
        f"- {memory['text']}"
        for memory in memories
    )

    return f"""
        Relevant long-term user memories:
        
        {memory_lines}
        
        Use these memories only if they help answer the current message.
        If a memory conflicts with the current message, follow the current message.
        Do not mention memory retrieval to the user.
        """.strip()