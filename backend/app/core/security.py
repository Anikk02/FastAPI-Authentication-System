import hashlib 
import logging
from typing import Any
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

REFRESH_TOKEN_EXPIRE_DAYS = 7

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=10) #reduce round cost


def hash_password(password: str) -> str:
    try:
        hashed_password = pwd_context.hash(password)
        logger.info("Password hashed successfully")
        return hashed_password
    except Exception as e:
        logger.exception("Failed to hash password")
        raise RuntimeError(f"Password hashing error: {e}") from e


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        is_valid = pwd_context.verify(plain_password, hashed_password)

        if is_valid:
            logger.info("Password verification successful")
        else:
            logger.warning("Password verification failed")

        return is_valid
    except Exception as e:
        logger.exception("Failed to verify password")
        raise RuntimeError(f"Password verification error: {e}") from e


def create_access_token(data: dict[str, Any]) -> str:
    try:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire, 'type':'access'})

        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

        logger.info("Access token created successfully")
        return encoded_jwt
    except Exception as e:
        logger.exception("Failed to create access token")
        raise RuntimeError(f"Token creation error: {e}") from e


def decode_access_token(token: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        if payload.get('type') != "access":
            logger.warning("Invalid token type for access")
            return None
        
        logger.info("Access token decoded successfully")
        return payload
    except JWTError:
        logger.warning("Invalid or expired token")
        return None
    except Exception as e:
        logger.exception("Unexpected error while decoding access token")
        raise RuntimeError(f"Token decode error: {e}") from e

def create_refresh_token(data : dict)-> str:
    try:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        to_encode.update({'exp': expire, 'type':'refresh'})

        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

        logger.info("Refresh token created successfully")
        return encoded_jwt
    except Exception as e:
        logger.exception("Failed to create refresh token")
        raise RuntimeError(f"Refresh token error: {e}") from e
    

def hash_token(token: str) -> str:
    try:
        return hashlib.sha256(token.encode()).hexdigest()
    except Exception as e:
        logger.exception("Failed to hash token")
        raise RuntimeError(f"Token hashing error: {e}") from e
