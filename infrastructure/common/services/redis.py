from redis.asyncio import Redis, from_url

from settings.redis import RedisSettings


class RedisService:
    __client = None

    @staticmethod
    def get(settings: RedisSettings) -> Redis:
        if RedisService.__client is None:
            RedisService.__client = from_url(settings.url)
        return RedisService.__client
