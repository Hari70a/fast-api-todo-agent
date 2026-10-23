from os import getenv

from starlette import status
from starlette.exceptions import HTTPException

import requests

API_URL = getenv("API_BASE_PATH")

def get_all_todos(token: str):
    response = requests.get(f"{API_URL}/todos/", headers={"Authorization": f"Bearer {token}"},)
    try:
        response.raise_for_status()
        response_data = response.json()
        return response_data
    except requests.exceptions.HTTPError:
        error = response.json()["detail"]
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error)


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
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        detail = response.json()["detail"]
        if response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT:
            print(detail, "422 error details")
            response_data= detail[0]
            error = response_data["msg"].replace("String", response_data["loc"][1].title())
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=error)
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
        else:
            raise


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
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        detail = response.json()["detail"]
        if response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT:
            print(detail, "422 error details")
            response_data= detail[0]
            error = response_data["msg"].replace("String", response_data["loc"][1].title())
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=error)
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
        else:
            raise

def delete_todo(token: str, todo_id: str):
    print(todo_id, "Todo id %$$$$$")
    response = requests.delete(
        f"{API_URL}/todos/{todo_id}",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        error = response.json()["detail"]
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=error)
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error)
        else:
            raise

    return {
        "message": f"Todo {todo_id} is deleted successfully",
        "status_code": response.status_code,
    }

