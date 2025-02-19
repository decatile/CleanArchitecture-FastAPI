from application.exceptions.referral_code_not_exist import ReferralCodeNotExist
from application.exceptions.user_not_found import UserNotFound
from application.interfaces.referral_code_repository import ReferralCodeRepository
from application.schemas.referral_code import ReferralCodeResponseDTO
from application.interfaces.user_repository import UserRepository


class GetReferralCodeByEmailUseCase:
    def __init__(
        self, users: UserRepository, referral_codes: ReferralCodeRepository
    ) -> None:
        self.users = users
        self.referral_codes = referral_codes

    async def run(self, email: str) -> ReferralCodeResponseDTO | None:
        user = await self.users.find_by_email(email)
        if user is None:
            raise UserNotFound()
        code = await self.referral_codes.find_by_user_id(user.id)
        if code is None:
            raise ReferralCodeNotExist()
        return ReferralCodeResponseDTO(str(code.id))
