import logging

import redis.asyncio as redis

from redis.exceptions import (
    RedisError,
    ConnectionError,
    TimeoutError
)

from app.config import settings

logger = logging.getLogger(__name__)

try:
    redis_client = redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
        max_connections=100,
        socket_connect_timeout=5,
        socket_timeout=5
    )

    # Global Redis availability flag
    redis_available = False

    async def check_redis():
        global redis_available

        try:
            await redis_client.ping()

            redis_available = True

            logger.info(
                "Redis connected successfully"
            )

        except (ConnectionError, TimeoutError) as e:
            redis_available = False

            logger.warning(
                f"Redis unavailable: {e}"
            )

        except RedisError as e:
            redis_available = False

            logger.error(
                f"Redis error: {e}"
            )

        except Exception:
            redis_available = False

            logger.exception(
                "Unexpected Redis error"
            )

    logger.info(
        "Async Redis client initialized successfully"
    )

except Exception as e:
    logger.exception(
        "Failed to initialize Redis client"
    )

    raise RuntimeError(
        f"Redis initialization error: {e}"
    ) from e