from application.interfaces.user_repository import UserRepository


class GetReferralsByReferrerIDUseCase:
    def __init__(self, users: UserRepository) -> None:
        self.users = users

    async def run(self, referrer_id: int) -> list[str]:
        return [i.email for i in await self.users.find_all_by_ref(referrer_id)]
