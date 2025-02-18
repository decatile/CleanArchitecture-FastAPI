import jwt

from application.schemas.tokens import RefreshTokenResponseDTO
from settings.jwt import JwtSettings
from presenter.schemes.tokens_set import TokensSet
from presenter.schemes.jwt_object import JwtObject
from utils.datetime import utc_now


class JwtService:
    def __init__(self, settings: JwtSettings) -> None:
        self.settings = settings

    def write(self, token_response: RefreshTokenResponseDTO) -> TokensSet:
        access_token = jwt.encode(
            {
                "sub": str(token_response.user_id),
                "exp": int(utc_now().timestamp()) + self.settings.expires_in,
            },
            self.settings.key,
            "HS256",
        )
        return TokensSet(
            access_token,
            self.settings.expires_in,
            token_response.refresh_token,
            token_response.expires_in,
        )

    def read(self, value: str) -> JwtObject | None:
        try:
            obj = jwt.decode(value, self.settings.key, ["HS256"], verify=True)
            return JwtObject(int(obj["sub"]))
        except jwt.DecodeError:
            return None
