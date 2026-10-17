from google.genai import types
from .register_tools import get_all_todos_tool, add_todo_tool, update_todo_tool, delete_todo_tool

tool_config = types.GenerateContentConfig(
    system_instruction=(
        "If the user tells you their preferred name, remember it and "
        "address them by that name in all subsequent responses in this "
        "conversation, starting with your very next reply."
    ),
    tools=[
        types.Tool(
            function_declarations=[get_all_todos_tool]
        ),
        types.Tool(
            function_declarations=[add_todo_tool]
        ),
        types.Tool(
            function_declarations=[update_todo_tool]
        ),
        types.Tool(
            function_declarations=[delete_todo_tool]
        )
    ]
)

