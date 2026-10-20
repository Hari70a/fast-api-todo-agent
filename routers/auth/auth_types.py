from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    email:str
    username:str
    first_name:str
    last_name:str
    password:str
    role:str
    phone_number:str

class LoginWithToken(BaseModel):
    access_token: str
    token_type: str