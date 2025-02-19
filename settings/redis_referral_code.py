from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisReferralCodeSettings(BaseSettings):
    url: str
    expires_in: int

    model_config = SettingsConfigDict(env_prefix="REDIS_REFERRAL_CODE_")
