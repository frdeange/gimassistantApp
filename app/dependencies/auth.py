import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.user import User
from app.services.user_service import UserService
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load configuration from environment variables
SECRET_KEY = os.environ.get("AUTH_SECRET_KEY", "secret")
ALGORITHM = os.environ.get("AUTH_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("AUTH_EXPIRATION", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_service() -> UserService:
    """
    Function to get the user service instance.
    This enables dependency injection and simplifies testing.
    """
    return UserService()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create an access token (JWT) with the provided data.

    :param data: Dictionary containing the data to encode in the token.
    :param expires_delta: Optional expiration time delta. If not provided, a default value is used.
    :return: Encoded JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), user_service: UserService = Depends(get_user_service)) -> User:
    """
    Dependency function to retrieve the current user based on the provided JWT token.

    :param token: JWT token provided in the request.
    :param user_service: Instance of the user service.
    :return: User object corresponding to the token.
    :raises HTTPException: If the token is invalid or the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = user_service.get_user_by_username(username)
    if user is None:
        raise credentials_exception

    return user