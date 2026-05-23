import logging
import time
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.database import get_db, safe_execute
from app.core.redis import redis_get, redis_set, redis_client, redis_delete
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
from app.metrics.tracker import log_metric

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
)->UserResponse:
    try:
        logger.info(f"Registration attempt: {mask_email(user_data.email)}")

        result = await safe_execute(
            db,
            select(User.id).where(User.email == user_data.email)
        )
        existing_user = result.first()
        if existing_user:
            logger.warning(f"Registration failed: email already exists {mask_email(user_data.email)}")
            raise HTTPException(
                status_code=400,
                detail = "Email already registered"
            )
        
        #Hash Password
        hashed_password = await run_in_threadpool(
            hash_password, user_data.password
        )

        #Create User
        new_user = User(
            name = user_data.name,
            email = user_data.email,
            hashed_password=hashed_password
        )

        db.add(new_user)
        await db.flush() #get ID without full commit
        await db.refresh(new_user)
        await db.commit() #commit consistency

        logger.info(f"User registered successfully: user_id={new_user.id}, email={mask_email(user_data.email)}")

        return UserResponse.model_validate(new_user)
    
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
    
    start_total = time.perf_counter()
    try:
        logger.info(f"Login attempt for email={mask_email(user_data.email)}")
        
        # DB lookup timing
        start = time.perf_counter()
        result = await safe_execute(
            db,
            select(User.id,
                   User.email,
                   User.name, 
                   User.hashed_password, 
                   User.is_active,
                   User.role,
                   User.created_at).where(User.email == user_data.email)
        )
        log_metric("db_user_lookup_ms", (time.perf_counter() - start) * 1000)

        user = result.first()
        if user is None:
            logger.warning(f"Login failed: user not found for email={mask_email(user_data.email)}")
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )
        
        user_id, email, name, role, created_at, hashed_password, is_active = user
        
        # Threadpool timing
        start = time.perf_counter()
        is_valid = await run_in_threadpool(
            verify_password,
            user_data.password,
            hashed_password
        )
        log_metric("password_verify_threadpool_ms", (time.perf_counter() - start) * 1000)

        if not is_valid:
            logger.warning(f"Login failed: invalid password for email={mask_email(user_data.email)}")
            raise HTTPException(
                status_code=401,
                detail = "Invalid email or password"
            )
        
        if not is_active:
            logger.warning(f"Login denied: inactive user user_id={user_id}")
            raise HTTPException(
                status_code=403,
                detail = "Inactive user account"
            )
        
        access_token = create_access_token({'user_id':user_id})
        refresh_token = create_refresh_token({'user_id':user_id})

        hashed_access = hash_token(access_token)
        hashed_refresh_token = hash_token(refresh_token)

        # USER SNAPSHOT
        user_response = UserResponse(
            id=user_id,
            email=email,
            name=name,
            role=role,
            created_at=created_at
            is_active=is_active
        )

        # Store session data in Redis using pipeline
        start = time.perf_counter()

        try:
            pipe = redis_client.pipeline()

            #store session -> used for authentication
            pipe.set(
                f"session:{hashed_access}",
                user_response.model_dump_json(),
                ex=ACCESS_TOKEN_EXPIRES_SECONDS
            )
            
            #Store refresh token mapping -> used for token refresh
            pipe.set(
                f"refresh:{hashed_refresh_token}",
                str(user_id),
                ex=7 * 24 * 60 * 60
            )
        
            pipe.set(
                f"access_to_refresh:{hashed_access}",
                hashed_refresh_token,
                ex=ACCESS_TOKEN_EXPIRES_SECONDS
            )

            await pipe.execute()

        except Exception as e:
            # Fail fast -> avoid partial login state
            logger.exception("Redis pipeline failed")
            raise HTTPException(
                status_code=500,
                detail="Login temporarily unavailable"
            ) from e
        
        log_metric("redis_set_session_ms", (time.perf_counter() - start) * 1000)
        
        # Total login timing
        log_metric('login_total_ms', (time.perf_counter() - start_total) * 1000)
        logger.info(f"User logged in successfully: user_id={user_id}")
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

        #REDIS FIRST
        stored_user = await redis_get(f"refresh:{hashed_refresh}")

        if stored_user:
            logger.info(f"Redis HIT refresh user_id={user_id}")
        else:
            logger.info(f"Redis MISS -> DB fallback user_id={user_id}")

            #DB Validation (fallback)
            result = await db.execute(
                select(Session).where(Session.refresh_token_hash==hashed_refresh)
            )
            session = result.scalar_one_or_none()

            if not stored_user or session is None:
                raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    detail = "Refresh token expired or invalid"
                )
        
        #Issue new access token
        new_access_token = create_access_token({"user_id": user_id})

        hashed_access = hash_token(new_access_token)

        #Store session (fail-open)
        await redis_set(
            key=f"session:{hashed_access}",
            value=str(user_id),
            ttl=ACCESS_TOKEN_EXPIRES_SECONDS
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    
    except Exception:
        logger.exception("Refresh token error")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )
    
@router.post("/logout", status_code = 204)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    try:
        token = credentials.credentials
        hashed_access = hash_token(token)

        # get linked refresh token
        refresh_hash = await redis_get(
            f"access_to_refresh:{hashed_access}"
        )

        # delete access session
        await redis_delete(f"session:{hashed_access}")

        # delete mapping
        await redis_delete(f"access_to_refresh:{hashed_access}")

        # delete refresh session
        if refresh_hash:
            await redis_delete(f"refresh:{refresh_hash}")

            #delete from DB as well
            await db.execute(
                delete(Session).where(Session.refresh_token_hash == refresh_hash)
            )
            await db.commit()
        
        logger.info("User logged out completely")
        return Response(status_code=204)
    
    except Exception as e:
        logger.exception("Logout error")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = 'Internal server error'
        )

