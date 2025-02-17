from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID

from domain.entities.base import ExpiresAt, NewType
from domain.entities.user import UserID
from utils.datetime import utc_now


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
    def new(id: UUID, user_id: int, expires_in: int):
        return ReferralCode(
            id=ReferralCodeID(id),
            user_id=UserID(user_id),
            expires_at=ExpiresAt(utc_now() + timedelta(seconds=expires_in)),
        )
