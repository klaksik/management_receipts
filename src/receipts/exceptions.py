from fastapi import HTTPException
from starlette import status


class CredentialsException(HTTPException):
    """
    Exception raised for invalid credentials. Inherits from HTTPException.

    :param status_code: The HTTP status code to return (default is 401 Unauthorized)
    :param detail: Detail message to return in the response body
    :param headers: Additional headers to return in the response
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )