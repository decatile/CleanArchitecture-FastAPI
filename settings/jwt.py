from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtSettings(BaseSettings):
    key: str
    expires_in: int

    model_config = SettingsConfigDict(env_prefix="JWT_TOKEN_")
