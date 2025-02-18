from sqlalchemy.ext.asyncio import AsyncSession


class SQLRepositoryBase:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
