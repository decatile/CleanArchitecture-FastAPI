from datetime import timedelta
import json
from typing import Literal
from uuid import UUID
from redis.asyncio import Redis
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.referral_code import ReferralCode
from infrastructure.sql.models.referral_code import SQLReferralCode
from infrastructure.sql.repos.referral_code import SQLReferralCodeRepository
from settings.redis_referral_code import RedisReferralCodeSettings

class SQLRedisCachingReferralCodeRepository(SQLReferralCodeRepository):
    def __init__(
        self, session: AsyncSession, redis: Redis, settings: RedisReferralCodeSettings
    ) -> None:
        super().__init__(session)
        self.redis = redis
        self.settings = settings

    async def __get(self, id: str) -> ReferralCode | Literal["deleted", "none"]:
        resp = await self.redis.get(id)
        if resp is None:
            return "none"
        await self.redis.expire(id, timedelta(seconds=self.settings.expires_in))
        if resp == "del":
            return "deleted"
        obj = json.loads(resp)
        return ReferralCode.new(UUID(obj["id"]), obj["user_id"], obj["expires_at"])

    async def __add(self, code: ReferralCode) -> None:
        id = str(code.id)
        p = self.redis.pipeline(False)
        p.set(
            id,
            json.dumps(
                {
                    "id": str(code.id),
                    "user_id": code.user_id,
                    "expires_at": code.expires_at.timestamp(),
                }
            ),
        )
        p.expire(id, timedelta(seconds=self.settings.expires_in))
        await p.execute()

    async def __del(self, id: str) -> None:
        p = self.redis.pipeline()
        p.set(id, "del")
        p.expire(id, timedelta(minutes=self.settings.expires_in))
        await p.execute()

    async def __update(self, id: str) -> None:
        await self.redis.expire(id, timedelta(seconds=self.settings.expires_in))

    async def delete(self, id: str) -> bool:
        if not await super().delete(id):
            return False
        await self.__del(id)
        return True

    async def delete_by_user_id(self, user_id: int) -> bool:
        r = await self.session.execute(
            delete(SQLReferralCode)
            .filter_by(user_id=user_id)
            .returning(SQLReferralCode.id)
        )
        row = r.fetchone()
        if row is None:
            return False
        await self.__del(str(row.t[0]))
        return True

    async def find_by_id(self, id: str) -> ReferralCode | None:
        code = await self.__get(id)
        if code == "deleted":
            return None
        if isinstance(code, ReferralCode):
            await self.__update(id)
            return code
        code = await super().find_by_id(id)
        if code is None:
            return None
        await self.__add(code)
        return code
