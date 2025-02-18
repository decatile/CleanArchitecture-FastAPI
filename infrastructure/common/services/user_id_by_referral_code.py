from datetime import timedelta
from redis.asyncio import Redis
from application.interfaces.referral_code_repository import ReferralCodeRepository
from application.interfaces.user_id_by_referral_code_service import (
    UserIDByReferralCodeService,
)
from application.usecases.delete_referral_code import ReferralCodeNotExist
from settings.redis import RedisSettings


class RedisUserIDByReferralCodeService(UserIDByReferralCodeService):
    def __init__(
        self, repo: ReferralCodeRepository, redis: Redis, settings: RedisSettings
    ) -> None:
        self.repo = repo
        self.redis = redis
        self.settings = settings

    async def user_id_by_referral_code(self, code_id: str) -> int | None:
        redis_key = f"referral_code_2_user_id.{code_id}"
        user_id = await self.redis.get(redis_key)
        if user_id is not None:
            return int(user_id)
        code = await self.repo.find_by_id(code_id)
        if code is None:
            raise ReferralCodeNotExist()
        user_id = code.user_id.value
        redis_pipeline = self.redis.pipeline()
        redis_pipeline.set(redis_key, user_id)
        redis_pipeline.expire(
            redis_key, timedelta(seconds=self.settings.referral_code_expires_in)
        )
        await redis_pipeline.execute()
        return user_id
