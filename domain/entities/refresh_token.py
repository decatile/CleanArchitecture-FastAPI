from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.entities.base import ExpiresAt, NewType
from domain.entities.user import UserID


class RefreshTokenID(NewType[UUID]): ...


@dataclass(frozen=True)
class RefreshToken:
    id: RefreshTokenID
    user_id: UserID
    expires_at: ExpiresAt

    @property
    def expired(self):
        return self.expires_at.expired

    @staticmethod
    def new(id: UUID, user_id: int, expires_at: datetime):
        return RefreshToken(
            id=RefreshTokenID(id),
            user_id=UserID(user_id),
            expires_at=ExpiresAt(expires_at),
        )
