from redis.asyncio import Redis, from_url

from settings.redis_referral_code import RedisReferralCodeSettings


class RedisReferralCodeService:
    __client = None

    @staticmethod
    def get(settings: RedisReferralCodeSettings) -> Redis:
        if RedisReferralCodeService.__client is None:
            RedisReferralCodeService.__client = from_url(settings.url)
        return RedisReferralCodeService.__client
