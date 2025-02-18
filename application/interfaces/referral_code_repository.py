from abc import ABC, abstractmethod

from domain.entities.referral_code import ReferralCode


class ReferralCodeRepository(ABC):
    @abstractmethod
    async def create(self, user_id: int) -> ReferralCode: ...

    @abstractmethod
    async def delete_by_user_id(self, user_id: int) -> bool: ...
    
    @abstractmethod
    async def find_by_id(self, id: str) -> ReferralCode | None: ...

    @abstractmethod
    async def find_by_user_id(self, user_id: int) -> ReferralCode | None: ...
