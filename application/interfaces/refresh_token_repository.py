from abc import ABC, abstractmethod

from domain.entities.refresh_token import RefreshToken


class RefreshTokenRepository(ABC):
    @abstractmethod
    async def create(self, user_id: int, expires_in: int) -> RefreshToken: ...
