from typing import Optional
from pydantic import BaseModel, validator
from .validators import phone_number_must_be_valid


class UserActivate(BaseModel):
    phone_number: str
    token: str
    email: Optional[str]

    _verify_phone = validator("phone_number", allow_reuse=True)(
        phone_number_must_be_valid
    )


class UserCreate(BaseModel):
    phone_number: str
    email: Optional[str]
    password: str

    _verify_phone = validator("phone_number", allow_reuse=True)(
        phone_number_must_be_valid
    )


class Login(BaseModel):
    phone_number: str
    password: str

    _verify_phone = validator("phone_number", allow_reuse=True)(
        phone_number_must_be_valid
    )
