import redis.asyncio as redis
import logging
from backend.app.config import settings
from redis.exceptions import RedisError, ConnectionError, TimeoutError

logger = logging.getLogger(__name__)
try:
    redis_client = redis.Redis(
        host = 'localhost',
        port = 6379,
        db=0,
        decode_responses=True, #returns string instead of bytes
        max_connections = 100,
        socket_connect_timeout=1,
        socket_timeout=1
    )

    #global flag for redis availability check
    redis_available = False

    async def check_redis():
        global redis_available
        try:
            await redis_client.ping()
            redis_available = True
            logger.info("Redis connected")
        except (ConnectionError, TimeoutError) as e:
            redis_available = False
            logger.warning(f"Redis unavailable: {e}")
        except RedisError as e:
            redis_available = False
            logger.error(f"Redis error: {e}")
        except Exception:
            redis_available = False
            logger.exception("Unexpected Redis error")

    logger.info("Async Redis client initialized successfully")

except Exception as e:
    logger.exception("Failed to initialize Redis client")
    raise RuntimeError(f"Redis initialization error: {e}") from e

