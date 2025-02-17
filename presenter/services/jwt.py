import jwt

from application.schemas.tokens import RefreshTokenResponseDTO
from presenter.settings.jwt import JwtSettings
from presenter.routes.auth import TokensSet
from presenter.schemes.jwt_object import JwtObject
from utils.datetime import utc_now


class JwtService:
    def __init__(self, settings: JwtSettings) -> None:
        self.settings = settings

    def write(self, token_response: RefreshTokenResponseDTO) -> TokensSet:
        access_token = jwt.encode(
            {
                "sub": token_response.user_id,
                "exp": int(utc_now().timestamp())
                + self.settings.access_token_expires_in,
            },
            self.settings.access_token_key,
            "HS256",
        )
        return TokensSet(
            access_token,
            self.settings.access_token_expires_in,
            token_response.refresh_token,
            token_response.expires_in,
        )

    def read(self, value: str) -> JwtObject | None:
        try:
            obj = jwt.decode(value, self.settings.access_token_key, ["HS256"])
            return JwtObject(obj["sub"])
        except jwt.DecodeError:
            return None
