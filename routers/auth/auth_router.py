from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import or_
from starlette import status
from starlette.exceptions import HTTPException

from database.db_models.users import Users
from database.db_utils.db_dependency import db_dependency
from routers.auth.auth_types import CreateUserRequest, LoginWithToken
from routers.auth.auth_utils import authenticate_user, create_access_token, hash_password, validate_existing_user
from routers.auth.refresh_token_utils import create_refresh_token, validate_refresh_token, revoke_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    existing_user = validate_existing_user(db, create_user_request)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )
    create_user_model = Users(
        email = create_user_request.email,
        username= create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = hash_password(create_user_request.password),
        is_active = True,
        role= create_user_request.role,
        phone_number = create_user_request.phone_number
    )

    db.add(create_user_model)
    db.commit()

@router.post("/login", response_model=LoginWithToken)
async def login_with_token(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    authenticated_user = authenticate_user(form_data.username, form_data.password, db)

    if authenticated_user:
        access_token = create_access_token(authenticated_user.username, authenticated_user.id, authenticated_user.role, timedelta(minutes=15))

        # refresh_token = create_refresh_token(authenticated_user.id, timedelta(days=7), db)
        # response.set_cookie(
        #     key="refresh_token",
        #     value=refresh_token,
        #     httponly=True,
        #     secure=True, # for HTTPS only
        #     samesite="none",  # UI and API are on different sites (onrender.com is a public suffix)
        #     path="/auth",
        #     max_age=7*24*60*60,  # 7 days in seconds
        # )
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not authenticate the user" )

@router.post("/refresh", response_model=LoginWithToken)
async def refresh_authentication(response: Response, db: db_dependency, refresh_token: Annotated[str | None, Cookie()] = None):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found")

    record, user = validate_refresh_token(refresh_token, db)
    
    revoke_token(db, record)
    new_refresh_token = create_refresh_token(user.id, timedelta(days=7), db, family_id=record.family_id)
    new_access_token = create_access_token(user.username, user.id, user.role, timedelta(minutes=2))

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True, # for HTTPS only
        samesite="none",  # UI and API are on different sites (onrender.com is a public suffix)
        path="/auth",
        max_age=7*24*60*60,  # 7 days in seconds
    )
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
