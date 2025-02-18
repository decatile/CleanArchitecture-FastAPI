from datetime import datetime, timedelta
from application.interfaces.refresh_token_repository import RefreshTokenRepository
from domain.entities.refresh_token import RefreshToken
from infrastructure.sql.models.refresh_token import SQLRefreshToken
from infrastructure.sql.repos.base import SQLRepositoryBase
from utils.datetime import utc_now


class SQLRefreshTokenRepository(SQLRepositoryBase, RefreshTokenRepository):
    async def create(self, user_id: int, expires_in: int) -> RefreshToken:
        r = SQLRefreshToken(
            user_id=user_id, expires_at=utc_now() + timedelta(seconds=expires_in)
        )
        self.session.add(r)
        await self.session.flush()
        return RefreshToken.new(r.id, r.user_id, r.expires_at)
