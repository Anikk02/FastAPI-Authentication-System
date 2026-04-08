import redis.asyncio as redis
import logging
from app.config import settings

logger = logging.getLogger(__name__)
try:
    redis_client = redis.Redis(
        host = 'localhost',
        port = 6379,
        db=0,
        decode_responses=True, #returns string instead of bytes
        max_connections = 100
    )

    logger.info("Async Redis client initialized successfully")

except Exception as e:
    logger.exception("Failed to initialize Redis client")
    raise RuntimeError(f"Redis initialization error: {e}") from e

