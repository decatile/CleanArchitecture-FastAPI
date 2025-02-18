from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    url: str

    model_config = SettingsConfigDict(env_prefix="DB")
