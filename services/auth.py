import jwt
import uuid
import bcrypt
from fastapi import status
from sqlmodel import Session, select
from datetime import datetime, timedelta, timezone
from config.settings import get_settings
from sqlalchemy.exc import IntegrityError
from dtos.auth import TokenDTO
from exceptions.business import (
    LOGIN_ERROR,
    AlreadyExistsError,
    USER_ALREADY_EXISTS_ERROR,
    LoginError,
)
from models import User, commit, engine


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        get_settings().jwt_secret,
        algorithm=get_settings().jwt_algorithm,
    )
    return encoded_jwt


def authenticate_user(phone_number: str, password: str) -> TokenDTO:
    access_token_expires = timedelta(
        minutes=get_settings().jwt_expiration_minutes
    )
    user = get_user_by_phone_number(phone_number)
    if not user or not verify_password(
        password, user.password.encode("utf-8")
    ):
        raise LoginError(
            message="Incorrect phone number or password",
            code=LOGIN_ERROR,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return TokenDTO(access_token=access_token, token_type="bearer")


def create_user(phone_number: str, password: str, email: str) -> User:
    hash = get_password_hash(password)
    user = User(
        id=uuid.uuid4(),
        phone_number=phone_number,
        email=email,
        password=hash.decode("utf-8"),
    )
    try:
        commit(user)
    except IntegrityError:
        raise AlreadyExistsError(
            message="User with this phone number already exists",
            code=USER_ALREADY_EXISTS_ERROR,
            status_code=status.HTTP_409_CONFLICT,
        )
    return user


def get_user_by_id(user_id: uuid.UUID) -> User | None:
    with Session(engine) as session:
        user = session.get(User, user_id)
        return user


def get_user_by_phone_number(phone_number: str) -> User | None:
    with Session(engine) as session:
        statement = select(User).where(User.phone_number == phone_number)
        return session.exec(statement).first()


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)


def get_password_hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
