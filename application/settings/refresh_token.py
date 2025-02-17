from pydantic_settings import BaseSettings


class RefreshTokenSettings(BaseSettings):
    expires_in: int
