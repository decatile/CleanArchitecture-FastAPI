from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    db_url: str
