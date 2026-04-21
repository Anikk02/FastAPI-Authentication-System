import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.exc import SQLAlchemyError
#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db, safe_execute
from app.core.redis import redis_client
from redis.exceptions import RedisError
from app.config import settings
from app.schemas import RefreshTokenRequest
from app.models.user import User
from app.models.session_model import Session
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    hash_password, 
    verify_password,
    hash_token
)
from app.schemas import TokenResponse, UserLogin, UserRegister, UserResponse

logger = logging.getLogger(__name__)

security = HTTPBearer()

ACCESS_TOKEN_EXPIRES_SECONDS = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

router = APIRouter(prefix='/auth', tags=['Auth'])

def mask_email(email:str)->str:
    name, domain = email.split('@')
    if len(name)<=1:
        return f"@" + domain
    return f"{name[0]}***@" + domain

@router.post('/register', response_model=UserResponse, status_code=201)
async def register_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
)->User:
    try:
        logger.info(f"Registration attempt: {mask_email(user_data.email)}")

        result = await safe_execute(
            db,
            select(User).where(User.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
            logger.warning(f"Registration failed: email already exists {mask_email(user_data.email)}")
            raise HTTPException(
                status_code=400,
                detail = "Email already registered"
            )
        
        new_user = User(
            name = user_data.name,
            email = user_data.email,
            hashed_password= await run_in_threadpool(
                hash_password, user_data.password
            )
        )

        db.add(new_user)
        await db.flush()
        await db.refresh(new_user)

        logger.info(f"User registered successfully: user_id={new_user.id}, email={mask_email(user_data.email)}")
        return new_user
    except HTTPException:
        raise

    except SQLAlchemyError as e:
        logger.exception("Database error during user registration")
        raise HTTPException(
            status_code = 500,
            detail = "Database error during registration"
        ) from e
    except Exception as e:
        logger.exception("Unexpected error during user registration")
        raise HTTPException(
            status_code=500,
            detail = "Internal server error during registration"
        ) from e

@router.post('/login', response_model=TokenResponse, status_code=200)
async def login_user(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db)
)->TokenResponse:
    try:
        logger.info(f"Login attempt for email={mask_email(user_data.email)}")

        result = await safe_execute(
            db,
            select(User).where(User.email == user_data.email)
        )
        user = result.scalar_one_or_none()
        if user is None:
            logger.warning(f"Login failed: user not found for email={mask_email(user_data.email)}")
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )
        
        is_valid = await run_in_threadpool(
            verify_password,
            user_data.password,
            user.hashed_password
        )
        if not is_valid:
            logger.warning(f"Login failed: invalid password for email={mask_email(user_data.email)}")
            raise HTTPException(
                status_code=401,
                detail = "Invalid email or password"
            )
        
        if not user.is_active:
            logger.warning(f"Login denied: inactive user user_id={user.id}")
            raise HTTPException(
                status_code=403,
                detail = "Inactive user account"
            )
        
        access_token = create_access_token(data={'user_id':user.id})
        refresh_token = create_refresh_token({'user_id':user.id})

        hashed_access = hash_token(access_token)
        hashed_refresh_token = hash_token(refresh_token)

        # Store in Redis
        try:
            await redis_client.setex(
            f"session:{hashed_access}",
            ACCESS_TOKEN_EXPIRES_SECONDS,
            user.id
            )
        except RedisError:
            logger.warning("Redis unavailable -> skipping access session storage")

        try:
            await redis_client.setex(
            f"refresh:{hashed_refresh_token}",
            7 * 24 * 60 * 60, # 7 days
            user.id
            )
        except RedisError:
            logger.warning("Redis unavailable -> skipping refresh storage")
        
        # link access -> refresh
        try:
            await redis_client.setex(
            f"access_to_refresh:{hashed_access}",
            ACCESS_TOKEN_EXPIRES_SECONDS,
            hashed_refresh_token
            )
        except RedisError:
            logger.warning("Redis unavailable -> skipping link access")

        # Store session in DB
        session = Session(
            user_id = user.id,
            refresh_token_hash = hashed_refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=7)
        )

        db.add(session)
        await db.commit()

        logger.info(f"User logged in successfully: user_id={user.id}")
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type='bearer'
        )
    except HTTPException:
        raise

    except SQLAlchemyError as e:
        logger.exception("Database error during user login")
        raise HTTPException(
            status_code=500,
            detail="Database error during login"
        ) from e
    except Exception as e:
        logger.exception("Unexpected error during user login")
        raise HTTPException(
            status_code=500,
            detail = "Internal server error during login"
        ) from e
    

@router.post("/refresh", status_code = 200)
async def refresh_token(
    data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    token = data.refresh_token
    try:
        payload = decode_access_token(token)

        if payload is None or payload.get("type") != "refresh":
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid refresh token"
            )
        
        user_id = payload.get("user_id")

        hashed_refresh = hash_token(token)

        # Check Redis
        try:
            stored_user = await redis_client.get(f"refresh:{hashed_refresh}")
        except RedisError:
            logger.warning("Redis unavailable -> skipping refresh validation")
            stored_user = None
        
        #DB Check
        result = await db.execute(
            select(Session).where(Session.refresh_token_hash==hashed_refresh)
        )
        session = result.scalar_one_or_none()

        if not stored_user or session is None:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Refresh token expired or invalid"
            )
        
        #issue new access token
        new_access_token = create_access_token({"user_id": user_id})

        hashed_access = hash_token(new_access_token)

        try:
            await redis_client.setex(
            f"session:{hashed_access}",
            ACCESS_TOKEN_EXPIRES_SECONDS,
            str(user_id)
            )
        except RedisError:
            logger.warning("Redis unavailable -> skipping session store")

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    
    except Exception as e:
        logger.exception("Refresh token error")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )
    
@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        token = credentials.credentials
        hashed_access = hash_token(token)

        # get linked refresh token
        refresh_hash = await redis_client.get(
            f"access_to_refresh:{hashed_access}"
        )

        # delete access session
        await redis_client.delete(f"session:{hashed_access}")

        # delete mapping
        await redis_client.delete(f"access_to_refresh:{hashed_access}")

        # delete refresh session
        if refresh_hash:
            await redis_client.delete(f"refresh:{refresh_hash}")
        
        logger.info("User logged out completely")
        return {"message": "Logged out successfully"}
    
    except Exception as e:
        logger.exception("Logout error")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = 'Internal server error'
        )
