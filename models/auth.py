import uuid
from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default=None, primary_key=True)
    phone_number: str = Field(unique=True)
    email: Optional[str]
    password: str
    active: bool = Field(default=False)
