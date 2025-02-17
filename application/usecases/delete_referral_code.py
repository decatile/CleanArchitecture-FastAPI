from application.exceptions.referral_code_not_exist import ReferralCodeNotExist
from application.exceptions.user_not_found import UserNotFound
from application.interfaces.referral_code_repository import ReferralCodeRepository
from application.interfaces.user_repository import UserRepository


class DeleteReferralCodeUserCase:
    def __init__(
        self, users: UserRepository, referral_codes: ReferralCodeRepository
    ) -> None:
        self.users = users
        self.referral_codes = referral_codes

    async def run(self, user_id: int) -> None:
        user = await self.users.find_by_id(user_id)
        if user is None:
            raise UserNotFound()
        if not await self.referral_codes.delete_by_user_id(user.id.value):
            raise ReferralCodeNotExist()
