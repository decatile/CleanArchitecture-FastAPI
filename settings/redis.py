from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    url: str
    referral_code_expires_in: int

    model_config = SettingsConfigDict(env_prefix="REDIS_")
