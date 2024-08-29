from fastapi import HTTPException
from starlette import status


class InvalidCredentialsException(HTTPException):
    """Exception raised for invalid credentials."""

    def __init__(self):
        """Initialize the exception with a 401 status and an error message."""
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,  # Unauthorized status code
            detail="Incorrect username or password",   # Error detail message
            headers={"WWW-Authenticate": "Bearer"},    # Authentication header
        )