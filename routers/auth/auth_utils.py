from datetime import timedelta, datetime, timezone
from os import getenv
from pathlib import Path
import hashlib
from typing import Annotated

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import or_
from starlette import status

from database.db_models.users import Users
from routers.auth.auth_types import CreateUserRequest

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
SECRET_KEY = getenv("BASE64_SECRET_KEY")
ALGORITHM = "HS256"

oauth2bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

def _password_digest(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).digest()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(_password_digest(password), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(_password_digest(password), hashed_password.encode("utf-8"))

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()

    if user is None:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(username: str, user_id: str, user_role: str, expires_delta: timedelta):
    encode = { "sub":  username, "id": user_id, "role": user_role, "token_type": "access" }
    update_time= datetime.now(timezone.utc) + expires_delta

    encode.update({"exp": update_time})
    token = jwt.encode(encode, SECRET_KEY, algorithm = ALGORITHM)

    return token


def get_current_user(token: Annotated[str, Depends(oauth2bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_name = payload.get("sub")
        user_id = payload.get("id")
        user_role = payload.get("role")
        token_type = payload.get("token_type")

        if user_name is None or user_id is None or token_type != "access":
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail ="Could not authenticate the user")

        return {
            "id": user_id,
            "user_name": user_name,
            "user_role": user_role,
            "token_type": token_type
        }

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not found the user")
    

def create_refresh_token(user_id: str, expires_delta: timedelta):
    encode = { "sub":  user_id, "token_type": "refresh" }
    update_time= datetime.now(timezone.utc) + expires_delta

    encode.update({"exp": update_time})
    token = jwt.encode(encode, SECRET_KEY, algorithm = ALGORITHM)

    return token

def validate_refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")
        token_type = payload.get("token_type")

        if user_id is None or token_type != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        return {
            "user_id": user_id,
            "token_type": token_type
        }

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    

def validate_existing_user(db, request: CreateUserRequest):
    return db.query(Users).filter(
        or_(
            Users.username == request.username,
            Users.email == request.email
        )
    )