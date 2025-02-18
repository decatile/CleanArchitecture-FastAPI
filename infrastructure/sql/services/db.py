from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from presenter.settings.db import DBSettings


class SQLDatabaseService:
    __engine: AsyncEngine | None = None

    @staticmethod
    def session(settings: DBSettings) -> AsyncSession:
        if SQLDatabaseService.__engine is None:
            SQLDatabaseService.__engine = create_async_engine(settings.db_url)
        return AsyncSession(SQLDatabaseService.__engine)
