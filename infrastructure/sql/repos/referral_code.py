from datetime import timedelta

from sqlalchemy import delete, select
from application.interfaces.referral_code_repository import ReferralCodeRepository
from domain.entities.referral_code import ReferralCode
from infrastructure.sql.models.referral_code import SQLReferralCode
from infrastructure.sql.repos.base import SQLRepositoryBase
from utils.datetime import utc_now


class SQLReferralCodeRepository(SQLRepositoryBase, ReferralCodeRepository):
    async def create(self, user_id: int, expires_in: int) -> ReferralCode:
        c = SQLReferralCode(
            user_id=user_id, expires_at=utc_now() + timedelta(seconds=expires_in)
        )
        self.session.add(c)
        await self.session.flush()
        return ReferralCode.new(c.id, c.user_id, c.expires_at)

    async def delete_by_user_id(self, user_id: int) -> bool:
        r = await self.session.execute(
            delete(SQLReferralCode).filter_by(user_id=user_id)
        )
        return r.rowcount > 0

    async def find_by_id(self, id: str) -> ReferralCode | None:
        code = await self.session.get(SQLReferralCode, id)
        if code is None:
            return None
        return ReferralCode.new(code.id, code.user_id, code.expires_at)

    async def find_by_user_id(self, user_id: int) -> ReferralCode | None:
        c = await self.session.scalar(
            select(SQLReferralCode).filter_by(user_id=user_id)
        )
        if c is None:
            return None
        return ReferralCode.new(c.id, c.user_id, c.expires_at)
