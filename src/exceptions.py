from fastapi import HTTPException


class ReceiptNotFoundException(HTTPException):
    """
    Exception raised when a receipt is not found.

    :param detail: Detail message to return in the response body (default is "Receipt not found")
    """

    def __init__(self, detail: str = "Receipt not found"):
        super().__init__(status_code=400, detail=detail)


class InsufficientPaymentException(HTTPException):
    """
    Exception raised when the payment amount is insufficient to cover the total cost of items.

    :param detail: Detail message to return in the response body (default is "The amount you provided is not enough to cover the total cost of the items.")
    """

    def __init__(self, detail: str = "The amount you provided is not enough to cover the total cost of the items."):
        super().__init__(status_code=400, detail=detail)


class InvalidCredentialsException(HTTPException):
    """
    Exception raised for incorrect username or password during authentication.

    :param detail: Detail message to return in the response body (default is "Incorrect username or password")
    """

    def __init__(self, detail: str = "Incorrect username or password"):
        super().__init__(status_code=401, detail=detail)


class UsernameAlreadyRegistered(HTTPException):
    """
    Exception raised when trying to register a username that is already registered.

    :param detail: Detail message to return in the response body (default is "Username already registered")
    """

    def __init__(self, detail: str = "Username already registered"):
        super().__init__(status_code=400, detail=detail)