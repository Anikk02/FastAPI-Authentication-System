from fastapi import APIRouter
from app.core.redis import redis_client

router = APIRouter()

@router.get('/redis-test')
def redis_test():
    redis_client.set('test_key','hello_aniket')
    value = redis_client.get('test_key')
    return {'value':value}