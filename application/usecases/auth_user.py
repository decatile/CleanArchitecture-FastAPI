import bcrypt

from application.exceptions.email_does_not_exist import EmailNotExist
from application.exceptions.invalid_password import InvalidPassword
from application.interfaces.refresh_token_repository import RefreshTokenRepository
from application.interfaces.user_repository import UserRepository
from application.schemas.tokens import RefreshTokenResponseDTO
from settings.refresh_token import RefreshTokenSettings


class AuthUserUseCase:
    def __init__(
        self,
        users: UserRepository,
        refresh_tokens: RefreshTokenRepository,
        refresh_settings: RefreshTokenSettings,
    ) -> None:
        self.users = users
        self.refresh_tokens = refresh_tokens
        self.refresh_settings = refresh_settings

    async def run(self, email: str, password: str) -> RefreshTokenResponseDTO:
        user = await self.users.find_by_email(email)
        if user is None:
            raise EmailNotExist()
        if not bcrypt.checkpw(user.password.value.encode(), password.encode()):
            raise InvalidPassword()
        token = await self.refresh_tokens.create(
            user.id.value, self.refresh_settings.expires_in
        )
        return RefreshTokenResponseDTO(
            user.id.value,
            str(token.id.value), self.refresh_settings.expires_in
        )
