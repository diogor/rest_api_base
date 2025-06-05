from typing import Optional


USER_ALREADY_EXISTS_ERROR = "user_already_exists"
INVALID_CREDENTIALS_ERROR = "invalid_credentials"
INVALID_TOKEN_ERROR = "invalid_token"
USER_NOT_FOUND_ERROR = "user_not_found"
LOGIN_ERROR = "login_error"


class BaseException(Exception):
    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        status_code: int = 400,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code


class AlreadyExistsError(BaseException):
    pass


class NotFoundError(BaseException):
    pass


class LoginError(BaseException):
    pass


class AuthenticationError(BaseException):
    pass


class DatabaseError(BaseException):
    pass


class IntegrationError(BaseException):
    pass
