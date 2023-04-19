from typing import Optional


class BaseException(Exception):
    def __init__(self, message: str, code: Optional[str] = None):
        self.code = code
        self.message = message


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
