from requests import HTTPError

from database import data
import requests

from routers.todos.todo_router import CreateTodoRequest

todos = data.todos
API_URL = "http://localhost:8000"

def get_all_todos(token: str):
    response = requests.get(f"{API_URL}/todos/", headers={"Authorization": f"Bearer {token}"},)

    response.raise_for_status()

    response_data = response.json()
    return response_data


def add_todo(token: str, new_task_data):
    print(new_task_data, "new_task_data @@@@@")
    response = requests.post(
        f"{API_URL}/todos/create-todo",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=new_task_data
    )
    # if new_task is None:
    #     new_task = {ˀ
    #         "title": "Learn AI",
    #         "status": "pending",ˀ
    #         "priority": 3.
    #     }
    # new_task["id"] = len(todos) + 1ˀ
    # todos.append(new_task)

    response.raise_for_status()

    return {
        "message": "Todo created successfully",
        "status_code": response.status_code,
    }

def update_todo(token: str, update_task_data):
    payload = {
        key: value
        for key, value in update_task_data.items()
        if key != "todo_id"
    }
    response = requests.put(
        f"{API_URL}/todos/{update_task_data['todo_id']}",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload
    )
    print("Status:", response.status_code)
    print("Response:", response.text)
    print("Payload:", payload)
    # if new_task is None:
    #     new_task = {ˀ
    #         "title": "Learn AI",
    #         "status": "pending",ˀ
    #         "priority": 3.
    #     }
    # new_task["id"] = len(todos) + 1ˀ
    # todos.append(new_task)

    response.raise_for_status()

    return {
        "message": f"Todo {update_task_data['todo_id']} is updated successfully",
        "status_code": response.status_code,
    }

def delete_todo(token: str, todo_id: str):
    print(todo_id, "Todo isshfjdhfhfgh %$$$$$")
    response = requests.delete(
        f"{API_URL}/todos/{todo_id}",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    print("Status:", response.status_code)
    print("Response:", response.text)
    # if new_task is None:
    #     new_task = {ˀ
    #         "title": "Learn AI",
    #         "status": "pending",ˀ
    #         "priority": 3.
    #     }
    # new_task["id"] = len(todos) + 1ˀ
    # todos.append(new_task)

    response.raise_for_status()

    return {
        "message": f"Todo {todo_id} is deleted successfully",
        "status_code": response.status_code,
    }



def complete_todo(id):
    for todo in todos:
        if todo["id"] == id:
            todo["status"] = "Completed"
            break
