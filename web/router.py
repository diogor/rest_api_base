from typing import Annotated
import uuid
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security.oauth2 import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
import jwt
from jwt.exceptions import InvalidTokenError

from config.settings import get_settings
from dtos.auth import TokenDTO
from exceptions.business import (
    INVALID_CREDENTIALS_ERROR,
    INVALID_TOKEN_ERROR,
    USER_NOT_FOUND_ERROR,
    AuthenticationError,
)
from models.auth import User
from services.auth import authenticate_user, create_user, get_user_by_id
from web.dto import UserCreateDTO, UserCreateResponseDTO


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(
            token,
            get_settings().jwt_secret,
            algorithms=[get_settings().jwt_algorithm],
        )
        username = payload.get("sub")
        if username is None:
            raise AuthenticationError(
                message="Could not validate credentials",
                code=INVALID_CREDENTIALS_ERROR,
                status_code=401,
            )
    except InvalidTokenError:
        raise AuthenticationError(
            message="Invalid token",
            code=INVALID_TOKEN_ERROR,
            status_code=401,
        )

    user = get_user_by_id(uuid.UUID(username))
    if user is None:
        raise AuthenticationError(
            message="User not found",
            code=USER_NOT_FOUND_ERROR,
            status_code=401,
        )

    return user


base_router = APIRouter(tags=["base"])
auth_router = APIRouter(prefix="/auth", tags=["auth"])


@base_router.get("/")
async def index(user: Annotated[User, Depends(get_current_user)]) -> User:
    return user


@auth_router.post("/register")
async def register(user: UserCreateDTO) -> UserCreateResponseDTO:
    user_obj = create_user(**user.model_dump())
    return UserCreateResponseDTO(id=str(user_obj.id))


@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenDTO:
    token = authenticate_user(
        phone_number=form_data.username, password=form_data.password
    )
    return token
