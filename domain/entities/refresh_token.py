from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID

from domain.entities.base import ExpiresAt, NewType
from domain.entities.user import UserID
from utils.datetime import utc_now


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
    def new(id: UUID, user_id: int, expires_in: int):
        return RefreshToken(
            id=RefreshTokenID(id),
            user_id=UserID(user_id),
            expires_at=ExpiresAt(utc_now() + timedelta(seconds=expires_in)),
        )
