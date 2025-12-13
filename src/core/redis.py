# src/core/redis.py
from fastapi import Depends
from redis.asyncio import Redis
from src.config import setting
import json
from typing import Any

# Define redis_client at module level
redis_client: Redis | None = None

async def get_redis() -> Redis:
    global redis_client
    if not redis_client:
        redis_client = Redis.from_url(setting.REDIS_CACHE_URL, decode_responses=True)
    return redis_client

async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()
        await redis_client.connection_pool.disconnect()
        redis_client = None  # reset

class RedisService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str) -> Any | None:
        value = await self.redis.get(key)
        if value is not None:
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, expire: int | None = None) -> None:
        await self.redis.set(key, json.dumps(value), ex=expire)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def incr(self, key: str) -> int:
        return await self.redis.incr(key)