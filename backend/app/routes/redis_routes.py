import logging
from fastapi import APIRouter
from backend.app.core.redis import redis_client

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get('/redis-test')
async def redis_test():
    await redis_client.set('test_key','hello_aniket')
    value = await redis_client.get('test_key')

    logger.info("Redis test endpoint hit")
    return {'value':value}