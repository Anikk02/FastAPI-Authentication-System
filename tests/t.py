import asyncio
import redis.asyncio as redis

async def test():
    r = redis.Redis()
    await r.set('test','hello')
    val = await r.get('test')
    print(val)

asyncio.run(test())