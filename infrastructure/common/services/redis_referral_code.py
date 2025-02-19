from redis.asyncio import Redis, from_url

from settings.redis_referral_code import RedisReferralCodeSettings


class RedisReferralCodeService:
    __client = None

    @classmethod
    def get(cls, settings: RedisReferralCodeSettings) -> Redis:
        if cls.__client is None:
            cls.__client = from_url(settings.url)
        return cls.__client
