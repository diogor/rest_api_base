from fastapi import HTTPException, status
from exceptions.business import (
    AlreadyExistsError,
    NotFoundError,
    LoginError,
    AuthenticationError,
)
from models.auth import User
from services.user import (
    create_user,
    login,
    activate_user as activate_user_service,
)
from web.request.auth import UserCreate, Login, UserActivate
from web.response.auth import LoginResponse


def register(user: UserCreate) -> User:
    try:
        return create_user(
            phone_number=user.phone_number,
            password=user.password,
            email=user.email,
        )
    except AlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        )


def login_user(credentials: Login) -> LoginResponse:
    try:
        return LoginResponse(
            access_token=login(credentials.phone_number, credentials.password)
        )
    except (NotFoundError, LoginError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        )


def activate_user(user: UserActivate) -> User:
    try:
        return activate_user_service(user.phone_number, user.token)
    except (NotFoundError, LoginError, AuthenticationError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        )
