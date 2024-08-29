from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth import service
from src.auth.exceptions import InvalidCredentialsException
from src.auth.schemas import UserCreate, Token, UserLogin
from src.database import get_db

# Create a new FastAPI router for authentication
auth_router = APIRouter()


@auth_router.post("/register", response_model=Token)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user and return a token.

    :param user_in: User creation schema containing user details
    :param db: Asynchronous database session
    :return: A bearer token for the registered user
    """
    user = await service.create_user(db, user_in)  # Asynchronously create a new user
    access_token = await service.create_access_token({"sub": user.id, "username": user.username, "name": user.name})
    return Token(access_token=access_token, token_type="bearer")


@auth_router.post("/login", response_model=Token)
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Authenticate a user and return a token.

    :param user_in: User login schema containing username and password
    :param db: Asynchronous database session
    :return: A bearer token for the authenticated user
    :raises InvalidCredentialsException: If user authentication fails
    """
    user = await service.authenticate_user(db, user_in.username,
                                           user_in.password)  # Asynchronously authenticate the user
    if not user:
        raise InvalidCredentialsException()  # Raise an exception if authentication fails

    access_token = await service.create_access_token(
        data={"sub": user.id, "username": user.username, "name": user.name})
    return Token(access_token=access_token, token_type="bearer")