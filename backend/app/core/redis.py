import logging
import asyncio
import redis.asyncio as redis

from redis.exceptions import RedisError, ConnectionError, TimeoutError
from app.config import settings

logger = logging.getLogger(__name__)

#Create Redis client
redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    max_connections=20,
    socket_connect_timeout=2,
    socket_timeout=2,
    health_check_interval=30,
    ssl=True,
    ssl_cert_reqs=None #avoid cert issues
)

REDIS_TIMEOUT = 0.1 #100ms
async def redis_get(key: str):
    try:
        return await asyncio.wait_for(
            redis_client.get(key),
            timeout=REDIS_TIMEOUT  # 100ms max
        )
    except (RedisError, ConnectionError, TimeoutError, asyncio.TimeoutError):
        logger.warning("Redis GET failed → fallback")
        return None


#SET with timeout
async def redis_set(key: str, value: str, ttl: int = 300):
    try:
        await asyncio.wait_for(
            redis_client.setex(key, ttl, value),
            timeout=REDIS_TIMEOUT
        )
    except (RedisError, ConnectionError, TimeoutError, asyncio.TimeoutError):
        logger.warning("Redis SET failed → skipping cache")


#Safe session check
async def redis_exists(key: str):
    try:
        result = await asyncio.wait_for(
            redis_client.get(key),
            timeout=REDIS_TIMEOUT
        )
        return result == 1
    except Exception:
        logger.warning("Redis EXISTS failed → assuming valid")
        return True  # fail-open

#DELETE

async def redis_delete(key: str):
    try:
        await asyncio.wait_for(
            redis_client.delete(key),
            timeout=REDIS_TIMEOUT
        )
    except (RedisError, ConnectionError, TimeoutError, asyncio.TimeoutError):
        logger.warning(f"Redis DELETE failed -> skipping | key={key}")