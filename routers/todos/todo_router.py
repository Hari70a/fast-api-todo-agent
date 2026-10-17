from fastapi import APIRouter, HTTPException, params
from pydantic import BaseModel, Field
from starlette import status

from database.db_models.todos import Todos
from database.db_utils.user_dependency import user_dependency
from database.db_utils.db_dependency import db_dependency


router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

class CreateTodoRequest(BaseModel):
    title: str = Field(max_length=20)
    description: str = Field(min_length=12, max_length=80)
    priority: int = Field(gt=0)
    complete: bool
    
class UpdateTodoRequest(BaseModel):
    title: str | None = Field(default=None, max_length=20)
    description: str | None = Field(default=None, min_length=12, max_length=80)
    priority: int | None = Field(default=None, gt=0)
    complete: bool | None = Field(default=None)



@router.get("/", status_code=status.HTTP_200_OK)
async def get_todos(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.post("/create-todo", status_code=status.HTTP_201_CREATED)
async def add_new_todo(user: user_dependency, db: db_dependency, create_todo_request: CreateTodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    # Approach 1: Using direct mapping of pydantic objects
    create_todo_model = Todos(
        title = create_todo_request.title,
        description = create_todo_request.description,
        complete = create_todo_request.complete,
        priority = create_todo_request.priority,
        owner_id = user.get("id")
    )

    # Approach 2: Convert to dictionary using modeL_dump & unpack the key & values
    # create_todo_model = Todos(**create_todo_request.dict(), owner_id = user.get("id"))

    db.add(create_todo_model)
    db.commit()


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, update_todo_request: UpdateTodoRequest, todo_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    todo_to_update = db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user["id"]).first()

    if todo_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


    # Approach 1: Using loop of items and set attributes
    for field, value in update_todo_request.model_dump(exclude_unset=True).items():
        setattr(todo_to_update, field, value)
    setattr(todo_to_update, "owner_id", user["id"])

    # Approach 2: Direct updates using dot operator
    # todo_to_update.title = update_todo_request.title
    # todo_to_update.description = update_todo_request.description
    # todo_to_update.priority = update_todo_request.priority
    # todo_to_update.complete = update_todo_request.complete
    # todo_to_update.owner_id = user.get("id")
    #
    db.add(todo_to_update)
    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    todo_to_delete = db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user["id"]).first()
    
    if todo_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    db.delete(todo_to_delete)
    db.commit()
