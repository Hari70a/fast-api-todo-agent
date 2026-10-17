from google.genai import types

get_all_todos_tool = types.FunctionDeclaration(
    name="get_all_todos",
    description="Show all todos",
    parameters={
        "type": "OBJECT",
        "properties": {}
    }
)

add_todo_tool = types.FunctionDeclaration(
    name="add_todo",
    description="Add or create a new todo",
    parameters={
        "type": "OBJECT",
        "properties": {
            "title": {
                "type":"STRING",
                "description": "Title of the task"
            },
            "description": {
                "type": "STRING",
                "description": "The comprehensive description of the task"
            },
            "priority": {
                "type": "INTEGER",
                "description": "Priority of the task"
            },
            "complete": {
                "type": "BOOLEAN",
                "description": "Indicates whether the task is completed"
            },
        },
        "required": ["title", "description", "priority"]
    }
)

update_todo_tool = types.FunctionDeclaration(
    name="update_todo",
    description="Update the existing todo",
    parameters={
        "type": "OBJECT",
        "properties": {
            "todo_id": {
              "type": "STRING",
                "description": "The id of the todo to be updated"
            },
            "title": {
                "type":"STRING",
                "description": "Title of the task"
            },
            "description": {
                "type": "STRING",
                "description": "The comprehensive description of the task"
            },
            "priority": {
                "type": "INTEGER",
                "description": "Priority of the task"
            },
            "complete": {
                "type": "BOOLEAN",
                "description": "Indicates whether the task is completed"
            },
        },
        "required": ["todo_id"]
    }
)

delete_todo_tool = types.FunctionDeclaration(
    name="delete_todo",
    description="Delete the unwanted todo",
    parameters={
        "type": "OBJECT",
        "properties": {
            "todo_id": {
              "type": "STRING",
                "description": "The id of the todo to be updated"
            }
        },
        "required": ["todo_id"]
    }
)