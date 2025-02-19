from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from uuid import UUID

from domain.entities.base import ExpiresAt
from domain.entities.user import UserID
from utils.datetime import utc_now


RefreshTokenID = NewType("RefreshTokenID", UUID)


@dataclass(frozen=True)
class RefreshToken:
    id: RefreshTokenID
    user_id: UserID
    expires_at: ExpiresAt

    @property
    def expired(self):
        return self.expires_at <= utc_now()

    @staticmethod
    def new(id: UUID, user_id: int, expires_at: datetime):
        return RefreshToken(
            id=RefreshTokenID(id),
            user_id=UserID(user_id),
            expires_at=ExpiresAt(expires_at),
        )
