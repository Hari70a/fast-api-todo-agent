from functools import partial

from database.db_functions import get_all_todos, add_todo, update_todo, delete_todo

# tool_mapper = {
#     "get_all_todos": get_all_todos,
#     "add_todo": add_todo
# }

def create_tool_mapper(token: str):
    return{
        "get_all_todos": partial(get_all_todos, token),
        "add_todo": partial(add_todo, token),
        "update_todo": partial(update_todo, token),
        "delete_todo": partial(delete_todo, token)
    }