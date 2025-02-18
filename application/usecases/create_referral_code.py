from application.exceptions.referral_code_already_exist import ReferralCodeAlreadyExist
from application.exceptions.user_not_found import UserNotFound
from application.interfaces.referral_code_repository import ReferralCodeRepository
from application.interfaces.user_repository import UserRepository
from application.schemas.referral_code import ReferralCodeResponseDTO


class CreateReferralCodeUserCase:
    def __init__(
        self, users: UserRepository, referral_codes: ReferralCodeRepository
    ) -> None:
        self.users = users
        self.referral_codes = referral_codes

    async def run(self, user_id: int, lifetime: int) -> ReferralCodeResponseDTO:
        user = await self.users.find_by_id(user_id)
        if user is None:
            raise UserNotFound()
        if (await self.referral_codes.find_by_user_id(user.id.value)) is not None:
            raise ReferralCodeAlreadyExist()
        code = await self.referral_codes.create(user.id.value, lifetime)
        return ReferralCodeResponseDTO(str(code.id.value))
