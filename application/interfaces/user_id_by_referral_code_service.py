from abc import ABC, abstractmethod


#
# Нужно чтобы добавить в пайплайн inmemory БД для быстрого маппинга (ref -> id)
#
class UserIDByReferralCodeService(ABC):
    @abstractmethod
    async def user_id_by_referral_code(self, code_id: str) -> int | None: ...
