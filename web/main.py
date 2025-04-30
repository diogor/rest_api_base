import sentry_sdk
from fastapi import Depends, FastAPI, Request
from fastapi_oauth2.middleware import OAuth2Middleware, Auth, User
from fastapi_oauth2.config import OAuth2Config, OAuth2Client
from fastapi_oauth2.router import router as oauth2_router
from fastapi_oauth2.security import OAuth2
from social_core.backends import open_id_connect
from config.settings import SENTRY_DSN, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRES, OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, OIDC_ENDPOINT


sentry_sdk.init(
    dsn=SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)


async def on_auth(auth: Auth, user: User):
    ...

oauth2 = OAuth2()

class OIDConnect(open_id_connect.OpenIdConnectAuth):
    OIDC_ENDPOINT = OIDC_ENDPOINT


oauth_config = OAuth2Config(
    allow_http=True,
    jwt_secret=JWT_SECRET,
    jwt_expires=JWT_EXPIRES,
    jwt_algorithm=JWT_ALGORITHM,
    clients=[
        OAuth2Client(
            backend=OIDConnect,
            client_id=OAUTH_CLIENT_ID,
            client_secret=OAUTH_CLIENT_SECRET,
        )
    ]
)

app = FastAPI()
app.add_middleware(OAuth2Middleware, config=oauth_config, callback=on_auth)
app.include_router(oauth2_router)


@app.get("/")
async def index(request: Request,  _: str = Depends(oauth2)):
    return {"user": request.user}

