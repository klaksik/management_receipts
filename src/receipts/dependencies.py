from datetime import timezone, datetime
from typing import Optional
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src import config
from src.auth.models import User
from src.database import get_db
from src.receipts.exceptions import CredentialsException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """
    Retrieve the user ID from the JWT token.

    :param token: OAuth2 token passed via the Authorization header
    :return: User ID extracted from the token
    :raises CredentialsException: If the token is invalid or expired
    """
    try:
        # Decode the JWT token
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.ALGORITHM])
        user_id: str = payload.get("sub")
        exp: int = payload.get("exp")

        if user_id is None or exp is None:
            raise CredentialsException()

        # Check if the token has expired
        if datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise CredentialsException()

    except PyJWTError:
        raise CredentialsException()

    return user_id


async def get_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    """
    Retrieve the current user based on the JWT token.

    :param token: OAuth2 token passed via the Authorization header
    :param db: Asynchronous database session
    :return: User object retrieved from the database
    :raises CredentialsException: If the token is invalid, expired, or the user is not found
    """
    try:
        # Decode the JWT token
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        exp: Optional[int] = payload.get("exp")

        if user_id is None or exp is None:
            raise CredentialsException()

        # Check if the token has expired
        if datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise CredentialsException()

        # Query the database to get the user
        async with db as session:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalars().one_or_none()

            if user is None:
                raise CredentialsException()

        return user

    except PyJWTError:
        raise CredentialsException()
