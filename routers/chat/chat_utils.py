from pathlib import Path
from typing import Generator

from google import genai
from google.genai import types
from dotenv import load_dotenv
from os import getenv
import json
import uuid
from pydantic import BaseModel

from py_tools.tool_config import tool_config
from routers.chat.conversation_store import load_history, save_history

from utils.tool_mapper import create_tool_mapper

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = genai.Client(
    api_key=getenv("GEMINI_API_KEY")
)

MODEL = "models/gemini-flash-lite-latest"

available_models = [
    model.name
    for model in client.models.list()
    if "generateContent" in model.supported_actions and model
]

print(available_models,"available models")

class GenerateContentResponse(BaseModel):
    answer: str
    chat_id: str

conversations = {}

def form_server_sent_event(payload: dict):
    return f"data: {json.dumps(payload, default=str)}\n\n"

def form_conversation(user_id: str):
    new_chat_id = uuid.uuid4().hex
    chat = client.chats.create(
        model=MODEL,
        config=tool_config
    )
    conversations[new_chat_id] = {
        "user_id": user_id,
        "chat": chat
    }
    return new_chat_id, chat

def get_chat(chat_id: str | None, user_id: str, db):
    if chat_id:
        conversation = conversations.get(chat_id)
        # if conversation is None or conversation["user_id"] != user_id:
        #     raise ValueError("Chat not found")
        if conversation:
            return chat_id, conversation["chat"]
        
        stored_history = load_history(db, chat_id, user_id)
        if stored_history is None:
            chat = client.chats.create(model=MODEL, config=tool_config)
        else:
            chat = client.chats.create(model=MODEL, config=tool_config, history=stored_history)
        conversations[chat_id] = {"user_id": user_id, "chat": chat}
        return chat_id, chat

    return form_conversation(user_id)

def generate_content(
    question: str,
    token: str,
    user_id: str,
    db,
    chat_id: str | None = None
) -> GenerateContentResponse:
    chat_id, chat = get_chat(chat_id, user_id, db)
    
    response = chat.send_message(question)

    while response.function_calls:
        if response.function_calls:
            function_call = response.function_calls[0]
            tool_mapper = create_tool_mapper(token)
            tool_function = tool_mapper[function_call.name]

            if function_call.args:
                if function_call.name == "delete_todo":
                    result = tool_function(**dict(function_call.args))
                else:
                    result = tool_function(function_call.args)
            else:
                result = tool_function()
            function_response = types.Part.from_function_response(
                name=function_call.name,
                response={"result": result}
            )
            response = chat.send_message(function_response)

    save_history(db, chat_id, user_id, chat.get_history(curated=True))
    return { "answer": response.text, "chat_id": chat_id }

def generate_content_stream(
    question: str,
    token: str,
    user_id: str,
    db,
    chat_id: str | None = None
) -> Generator[str]:
    #  Testing streams using SSE events below
    # Simple example for SSE
    # text1 = "Starting"
    # text2 = "content"
    # text3 = "generation..."
    # chat_id = uuid.uuid4().hex
    # print({"user_id": user_id, "chat_id": chat_id}, "User Od @@@@@@")
    # if token:
    #     yield f"data: {json.dumps({'type': 'token', 'text': text1})}\n\n"
    #     sleep(1)
    #     yield f"data: {json.dumps({'type': 'token', 'text': text2})}\n\n"
    #     sleep(1)
    #     yield f"data: {json.dumps({'type': 'token', 'text': text3})}\n\n"
    #     sleep(1)
    #     yield f"data: {json.dumps({'type': 'done'})}\n\n"
    # else:
    #     yield f"data: {json.dumps({'type': 'error', 'text': 'No token provided'})}\n\n"

    print(f"generate_content: incoming chat_id={chat_id!r}")

    if not token:
        yield form_server_sent_event({ "type": "error", "text": "Not authorized to perform the action"})
        return

    try:
        chat_id, chat = get_chat(chat_id, user_id, db)
        yield form_server_sent_event({"type": "meta", "chat_id": chat_id})
        tool_mapper = create_tool_mapper(token)
        message = question

        while True:
            pending_calls = []

            for chunk in chat.send_message_stream(message):
                if chunk.text:
                    yield form_server_sent_event({"type": "token", "text": chunk.text})
                if chunk.function_calls:
                    pending_calls.extend(chunk.function_calls)

            if not pending_calls:
                break

            function_responses = []
            for fc in pending_calls:
                args = dict(fc.args) if fc.args else {}
                yield form_server_sent_event({"type": "tool_call", "name": fc.name, "args": args})

                tool_function = tool_mapper[fc.name]
                if not args:
                    result = tool_function()
                elif fc.name == "delete_todo":
                    result = tool_function(**args)
                else:
                    result = tool_function(fc.args)

                yield form_server_sent_event({"type": "tool_result", "name": fc.name, "text": result})
                function_responses.append(
                    types.Part.from_function_response(name=fc.name, response={"result": result})
                )

            message = function_responses

        save_history(db, chat_id, user_id, chat.get_history(curated=True))
        yield form_server_sent_event({"type": "done", "chat_id": chat_id})

    except Exception as e:
        print(e, "Exception in chat utils")
        error = str(e).split(": ")[1]
        yield form_server_sent_event({"type": "error", "text": error})
