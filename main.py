from fastapi import FastAPI

from database.db_engine import engine, Base
from routers.auth import auth_router
from routers.chat import chat_router
from routers.todos import todo_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://todo-assistant-ui.onrender.com"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
    return { "status": "healthy" }

app.include_router(auth_router.router)
app.include_router(todo_router.router)
app.include_router(chat_router.router)