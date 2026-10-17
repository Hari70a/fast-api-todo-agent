from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from google.genai.errors import ServerError
from pydantic import BaseModel
from starlette import status

from database.db_utils.db_dependency import db_dependency
from database.db_utils.user_dependency import user_dependency
from routers.auth.auth_utils import oauth2bearer
from routers.chat.chat_utils import generate_content, generate_content_stream

router = APIRouter(
    prefix="/chats",
    tags=["chats"]
)

class StreamChatRequest(BaseModel):
    chat_id: str
    question: str

@router.get("/")
def ask_questions(
    user: user_dependency,
    db: db_dependency,
    token: Annotated[str, Depends(oauth2bearer)],
    question: str,
    chat_id: str = None
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't authenticate the userˀ")

    response = generate_content(question, token, user["id"], db, chat_id)
    # try:
    #     response = generate_content(question, token, user["id"], chat_id)
    # except ValueError:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Chat not found"
    #     )
    return response

@router.post("/stream")
def ask_questions_stream(user: user_dependency, token: Annotated[str, Depends(oauth2bearer)], db: db_dependency, chat_request: StreamChatRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't authenticate the user")

    return StreamingResponse(
        generate_content_stream(chat_request.question, token, user["id"], db, chat_request.chat_id),
        media_type="text/event-stream"
    )
