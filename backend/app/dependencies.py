import logging
import hashlib
from redis.exceptions import RedisError

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.core.security import decode_access_token
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.core.redis import redis_client, redis_available
import redis.asyncio as redis
from backend.app.schemas import UserResponse

logger = logging.getLogger(__name__)
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:

    try:
        token = credentials.credentials
        payload = decode_access_token(token)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        # check token type
        if payload.get("type") != "access":
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid token type"

            )

        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Step 1: SESSION VALIDATION
        hashed_token = hashlib.sha256(token.encode()).hexdigest()
        session_key = f"session:{hashed_token}"
        
        #executes if redis available
        if redis_available:
            try:
                session_exists = await redis_client.get(session_key)
                if not session_exists:
                    raise HTTPException(
                        status_code = status.HTTP_401_UNAUTHORIZED,
                        detail = "Session expired or revoked"
                    )
            except RedisError:
                logger.warning("Redis unavailable -> skipping session check")

        # Step 2: USER CACHE

        cache_key = f"user:{user_id}"

        # 1. Try Redis first
        if redis_available:
            try:
                cached_user = await redis_client.get(cache_key)
                if cached_user:
                    logger.info(f"Cache HIT user_id={user_id}")
                    return UserResponse.model_validate_json(cached_user)
            except RedisError:
                logger.warning("Redis unavailable → skipping cache GET")

        # 2. Fallback to DB
        logger.info(f"Cache MISS user_id={user_id}")
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            logger.warning(f"User not found user_id={user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        if not user.is_active:
            logger.warning(f"Inactive user user_id={user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user account"
            )

        # 3. Convert to schema
        user_response = UserResponse.model_validate(user)

        # 4. Store in Redis (TTL = 5 minutes)
        if redis_available:
            try:
                await redis_client.setex(
                    cache_key,
                    300,
                    user_response.model_dump_json()
                )
            except RedisError:
                logger.warning("Redis unavailable → skipping cache SET")

        return user_response

    except HTTPException:
        raise

    except Exception as e:
        logger.exception("Unexpected error while authenticating current user")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication"
        ) from e