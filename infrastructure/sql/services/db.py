from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from settings.db import DBSettings


class SQLDatabaseService:
    __engine: AsyncEngine | None = None

    @staticmethod
    def get(settings: DBSettings) -> AsyncSession:
        if SQLDatabaseService.__engine is None:
            SQLDatabaseService.__engine = create_async_engine(settings.url)
        return AsyncSession(SQLDatabaseService.__engine)
