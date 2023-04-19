import random
import redis
from typing import Optional
from twilio.rest import Client
from string import hexdigits
from datetime import datetime, timedelta
from sqlmodel import Session
import jwt
import bcrypt
from config import settings
from models import engine
from models.auth import User
from exceptions.business import AuthenticationError


redis_client = redis.from_url(settings.REDIS_URL)


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def make_jwt_token(user: User) -> str:
    return jwt.encode(
        {"id": user.id, "exp": datetime.utcnow() + timedelta(days=1)},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def check_user_token(token: str) -> Optional[User]:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        with Session(engine) as session:
            user = session.get(User, payload["id"])
        return user
    except jwt.ExpiredSignatureError:
        raise AuthenticationError(message="Token expired.")
    except jwt.InvalidTokenError:
        raise AuthenticationError(message="Invalid token.")


def set_token(user: User) -> str:
    token = "".join(random.choice(hexdigits) for _ in range(4)).upper()
    redis_client = redis.from_url(settings.REDIS_URL)
    redis_client.set(f"TOKEN:{user.phone_number}", token)
    return token


def get_token(user: User) -> str:
    token = redis_client.get(f"TOKEN:{user.phone_number}")
    if not token:
        raise AuthenticationError(message="Token not found.")
    return token.decode("utf-8")


def delete_token(user: User):
    redis_client.delete(f"TOKEN:{user.phone_number}")


def send_token(user: User):
    token = redis_client.get(f"TOKEN:{user.phone_number}").decode("utf-8")
    if not token:
        token = set_token(user)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=user.phone_number,
        messaging_service_sid=settings.TWILIO_MESSAGE_SERVICE_SID,
        body=f"Seu código de confirmação: {token}",
    )
