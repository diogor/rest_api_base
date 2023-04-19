import sentry_sdk
from fastapi import FastAPI
from config.settings import SENTRY_DSN
from .controllers.auth import (
    register,
    login_user,
    activate_user as activate_user_controller,
)
from .request.auth import UserCreate, Login, UserActivate
from .response.auth import User, LoginResponse

from .middleware.authorization import BasicAuthBackend, CustomAuthMiddleware


sentry_sdk.init(
    dsn=SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)


app = FastAPI()

app.add_middleware(CustomAuthMiddleware, backend=BasicAuthBackend())


@app.post("/auth/register")
async def register_user(user: UserCreate) -> User:
    return User(**register(user).dict())


@app.post("/auth/activate")
async def activate_user(user: UserActivate):
    activate_user_controller(user)


@app.post("/auth/login")
async def user_login(credentials: Login) -> LoginResponse:
    return login_user(credentials)
