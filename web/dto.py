from pydantic import BaseModel


class UserCreateDTO(BaseModel):
    phone_number: str
    email: str | None = None
    password: str


class UserCreateResponseDTO(BaseModel):
    id: str
