import bcrypt

from application.exceptions.email_already_exist import EmailAlreadyExist
from application.interfaces.refresh_token_repository import RefreshTokenRepository
from application.interfaces.user_repository import UserCreateDTO, UserRepository
from application.schemas.tokens import RefreshTokenResponseDTO
from application.usecases.auth_user import RefreshTokenSettings


class RegisterUserUseCase:
    def __init__(
        self,
        users: UserRepository,
        refresh_tokens: RefreshTokenRepository,
        refresh_settings: RefreshTokenSettings,
    ) -> None:
        self.users = users
        self.refresh_tokens = refresh_tokens
        self.refresh_settings = refresh_settings

    async def run(
        self, referral_code: str | None, email: str, password: str
    ) -> RefreshTokenResponseDTO:
        if self.users.find_by_email(email) is not None:
            raise EmailAlreadyExist()
        user = await self.users.create(
            UserCreateDTO(
                referral_code,
                email,
                bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
            )
        )
        token = await self.refresh_tokens.create(
            user.id.value, self.refresh_settings.expires_in
        )
        return RefreshTokenResponseDTO(
            user.id.value, str(token.id.value), self.refresh_settings.expires_in
        )
