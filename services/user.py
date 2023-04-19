from typing import Optional
from sqlmodel import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from exceptions.business import AlreadyExistsError, LoginError, NotFoundError
from models.auth import User
from models import commit, engine, Session
from .authentication import (
    verify_password,
    make_jwt_token,
    hash_password,
    send_token,
    get_token,
    delete_token,
)


def list_users(active: bool = False) -> list[User]:
    with Session(engine) as session:
        statement = select(User)
        if active:
            statement = statement.where(User.active == True)
        return session.exec(statement).all()


def create_user(
    phone_number: str, password: str, email: Optional[str]
) -> User:
    user = User(
        phone_number=phone_number,
        email=email,
        password=hash_password(password).decode("utf-8"),
    )

    try:
        commit(user)
        send_token(user)
    except IntegrityError:
        raise AlreadyExistsError(message="User already exists")

    return user


def get_user_by_phone_number(phone_number: str) -> User:
    with Session(engine) as session:
        try:
            statement = select(User).where(User.phone_number == phone_number)
            return session.exec(statement).one()
        except NoResultFound:
            raise NotFoundError(message="User not found")


def verify_user_token(user: User, token: str) -> bool:
    return get_token(user) == token


def activate_user(phone_number: str, token: str) -> User:
    user = get_user_by_phone_number(phone_number)
    if verify_user_token(user, token):
        user.active = True
        commit(user)
        delete_token(user)
        return user
    raise LoginError(message="Invalid token")


def login(phone_number: str, password: str) -> str:
    if user := get_user_by_phone_number(phone_number):
        if not user.active:
            raise LoginError(code="INACTIVE", message="Inactive user")
        if verify_password(password, user.password):
            return make_jwt_token(user)
        raise LoginError(message="Invalid password")

    raise NotFoundError(message="User not found")
