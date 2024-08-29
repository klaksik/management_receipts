from typing import Dict, Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import aiobcrypt
from src.auth import models, schemas
from datetime import datetime, timedelta, timezone
import jwt
from src import config
from src.exceptions import UsernameAlreadyRegistered


async def get_password_hash(password: str) -> str:
    """
    Generate a hashed password.

    :param password: Plain text password
    :return: Hashed password
    """
    salt = await aiobcrypt.gensalt()
    hashed_password = await aiobcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify whether a plain password matches the hashed password.

    :param plain_password: Plain text password
    :param hashed_password: Hashed password
    :return: Boolean indicating password match
    """
    # Encode both plain password and hashed password to bytes
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return await aiobcrypt.checkpw(plain_password_bytes, hashed_password_bytes)


async def create_user(db: AsyncSession, user_in: schemas.UserCreate):
    """
    Create a new user with a hashed password.

    :param db: Asynchronous database session
    :param user_in: Schema containing new user details
    :return: Newly created user object
    :raises UsernameAlreadyRegistered: If the username is already registered
    """
    async with db as session:
        # Check if a user with the same username already exists
        stmt = select(models.User).filter_by(username=user_in.username)
        result = await session.execute(stmt)
        existing_user = result.scalars().first()

        if existing_user:
            raise UsernameAlreadyRegistered()

        # Hash the user's password
        hashed_password = await get_password_hash(user_in.password)
        db_user = models.User(
            username=user_in.username,
            name=user_in.name,
            hashed_password=hashed_password
        )

        db.add(db_user)
        try:
            await db.commit()  # Asynchronous commit
            await db.refresh(db_user)  # Asynchronous refresh
        except IntegrityError:
            await db.rollback()
            raise UsernameAlreadyRegistered()

    return db_user


async def authenticate_user(db: AsyncSession, username: str, password: str):
    """
    Authenticate a user by username and password.

    :param db: Asynchronous database session
    :param username: Username input
    :param password: Password input
    :return: User object if authenticated, None otherwise
    """
    stmt = select(models.User).filter_by(username=username)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if user and await verify_password(password, user.hashed_password):
        return user

    return None


async def create_access_token(data: Dict[str, any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT token.

    :param data: Dictionary containing token data
    :param expires_delta: Time duration until token expiration
    :return: Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.ALGORITHM)