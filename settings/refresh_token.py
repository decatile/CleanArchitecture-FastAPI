from pydantic_settings import BaseSettings, SettingsConfigDict


class RefreshTokenSettings(BaseSettings):
    expires_in: int
    
    model_config = SettingsConfigDict(env_prefix='REFRESH_TOKEN')
