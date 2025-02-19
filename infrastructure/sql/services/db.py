from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from settings.db import DBSettings


class SQLDatabaseService:
    __engine: AsyncEngine | None = None

    @classmethod
    def get(cls, settings: DBSettings) -> AsyncSession:
        if cls.__engine is None:
            cls.__engine = create_async_engine(settings.url)
        return AsyncSession(cls.__engine)
