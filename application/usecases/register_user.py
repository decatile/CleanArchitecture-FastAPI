import bcrypt

from application.exceptions.email_already_exist import EmailAlreadyExist
from application.exceptions.referral_code_not_exist import ReferralCodeNotExist
from application.interfaces.referral_code_repository import ReferralCodeRepository
from application.interfaces.refresh_token_repository import RefreshTokenRepository
from application.interfaces.user_repository import UserRepository
from application.schemas.tokens import RefreshTokenResponseDTO
from settings.refresh_token import RefreshTokenSettings


class RegisterUserUseCase:
    def __init__(
        self,
        users: UserRepository,
        refresh_tokens: RefreshTokenRepository,
        referral_codes: ReferralCodeRepository,
        refresh_settings: RefreshTokenSettings,
    ) -> None:
        self.users = users
        self.refresh_tokens = refresh_tokens
        self.referral_codes = referral_codes
        self.refresh_settings = refresh_settings

    async def run(
        self, referral_code: str | None, email: str, password: str
    ) -> RefreshTokenResponseDTO:
        if (await self.users.find_by_email(email)) is not None:
            raise EmailAlreadyExist()
        ref_id = None
        if referral_code is not None:
            code = await self.referral_codes.find_by_id(referral_code)
            if code is None:
                raise ReferralCodeNotExist()
            ref_id = code.user_id.value
        user = await self.users.create(
            ref_id,
            email,
            bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
        )
        token = await self.refresh_tokens.create(
            user.id.value, self.refresh_settings.expires_in
        )
        return RefreshTokenResponseDTO(
            user.id.value, str(token.id.value), self.refresh_settings.expires_in
        )
