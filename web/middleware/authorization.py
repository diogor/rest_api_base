from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette.authentication import (
    AuthenticationBackend,
    AuthCredentials,
    AuthenticationError,
)
from fastapi import status
from fastapi.responses import JSONResponse, Response
from services.authentication import check_user_token
from exceptions.business import (
    AuthenticationError as BusinessAuthenticationError,
)


class CustomAuthMiddleware(AuthenticationMiddleware):
    @staticmethod
    def default_on_error(conn: HTTPConnection, exc: Exception) -> Response:
        return JSONResponse(
            {"detail": str(exc)}, status_code=status.HTTP_401_UNAUTHORIZED
        )


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        method = request.scope.get("method")
        path = request.scope.get("path")

        if path in ["/docs", "/redoc", "/openapi.json"]:
            return

        if method == "POST" and path in [
            "/auth/register",
            "/auth/login",
            "/auth/activate",
        ]:
            return

        if "Authorization" not in request.headers:
            raise AuthenticationError("Token not found")

        auth = request.headers["Authorization"]
        try:
            token = auth.split("Token")[1].strip()
        except IndexError:
            raise AuthenticationError("Invalid token format.")

        try:
            user = check_user_token(token)
            if not user:
                raise AuthenticationError("Invalid token.")
            if not user.active:
                raise AuthenticationError("Inactive user.")
        except BusinessAuthenticationError as e:
            raise AuthenticationError(e.message)

        return AuthCredentials(["authenticated"]), user
