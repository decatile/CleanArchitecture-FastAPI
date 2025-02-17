from application.interfaces.user_repository import UserRepository


class GetReferralsByReferrerIDUseCase:
    def __init__(self, users: UserRepository) -> None:
        self.users = users

    async def run(self, referrer_id: int) -> list[int]:
        return [i.id.value for i in await self.users.find_all_by_ref(referrer_id)]
