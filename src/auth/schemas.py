from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    name: str = Field(
        ...,  # This means the field is required
        pattern=r"^[\p{L} ,.'-]{2,64}$",  # Validation pattern for the name
        description="User's full name. Allowed characters: letters, spaces, and punctuation marks."
    )
    username: str = Field(
        ...,  # This means the field is required
        pattern=r"^[a-zA-Z0-9_-]{2,20}$",  # Validation pattern for the username
        description="Username consisting of 2-20 alphanumeric characters, underscores, or hyphens."
    )
    password: str = Field(
        ...,  # This means the field is required
        pattern=r"^[A-Za-z0-9#?!@$%^&*+-]{8,128}$",  # Validation pattern for the password
        description="Password consisting of 8-128 characters including alphabets, numbers, and special symbols."
    )


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str = Field(
        ...,  # This means the field is required
        pattern=r"^[a-zA-Z0-9_-]{2,20}$",  # Validation pattern for the username
        description="Username consisting of 2-20 alphanumeric characters, underscores, or hyphens."
    )
    password: str = Field(
        ...,  # This means the field is required
        pattern=r"^[A-Za-z0-9#?!@$%^&*+-]{8,128}$",  # Validation pattern for the password
        description="Password consisting of 8-128 characters including alphabets, numbers, and special symbols."
    )


class Token(BaseModel):
    """Schema for the token response."""
    access_token: str  # The actual access token
    token_type: str  # The type of the token, usually 'bearer'


class TokenData(BaseModel):
    """Schema for token data."""
    username: str | None = None  # Username contained in the token, if available
