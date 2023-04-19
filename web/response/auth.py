from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    phone_number: str
    email: Optional[str]


class LoginResponse(BaseModel):
    access_token: str
