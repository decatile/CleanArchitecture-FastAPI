from application.interfaces.referral_code_repository import ReferralCodeRepository
from domain.entities.referral_code import ReferralCode


class CleanupingReferralCodeRepository(ReferralCodeRepository):
    def __init__(self, instance: ReferralCodeRepository) -> None:
        self.instance = instance

    async def create(self, user_id: int, expires_in: int) -> ReferralCode:
        return await self.instance.create(user_id, expires_in)

    async def delete(self, id: str) -> bool:
        return await self.instance.delete(id)

    async def delete_by_user_id(self, user_id: int) -> bool:
        return await self.instance.delete_by_user_id(user_id)

    async def find_by_id(self, id: str) -> ReferralCode | None:
        code = await self.instance.find_by_id(id)
        if code is None:
            return None
        if code.expired:
            await self.delete(id)
            return None
        return code

    async def find_by_user_id(self, user_id: int) -> ReferralCode | None:
        code = await self.instance.find_by_user_id(user_id)
        if code is None:
            return None
        if code.expired:
            await self.delete_by_user_id(user_id)
            return None
        return code
