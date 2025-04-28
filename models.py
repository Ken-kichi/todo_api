from typing import Union
from pydantic import BaseModel

class User(BaseModel):
    id: str
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    is_manager: Union[bool, None] = None
    disabled: Union[bool, None] = None

class UserForm(User):
    password:str

class UserRead(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user:User


class TokenData(BaseModel):
    email: Union[str, None] = None

class Task(BaseModel):
    user_id: str
    title: str
    description: str | None = None


class TaskRead(Task):
    id: str
    completed: bool

class Message(BaseModel):
    message: str

