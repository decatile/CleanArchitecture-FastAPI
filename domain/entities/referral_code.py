from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.entities.base import ExpiresAt, NewType
from domain.entities.user import UserID


class ReferralCodeID(NewType[UUID]): ...


@dataclass(frozen=True)
class ReferralCode:
    id: ReferralCodeID
    user_id: UserID
    expires_at: ExpiresAt

    @property
    def expired(self):
        return self.expires_at.expired

    @staticmethod
    def new(id: UUID, user_id: int, expires_at: datetime):
        return ReferralCode(
            id=ReferralCodeID(id),
            user_id=UserID(user_id),
            expires_at=ExpiresAt(expires_at),
        )
