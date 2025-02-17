from pydantic_settings import BaseSettings


class JwtSettings(BaseSettings):
    access_token_key: str
    access_token_expires_in: int
