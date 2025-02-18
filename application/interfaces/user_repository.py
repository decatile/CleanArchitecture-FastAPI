from abc import ABC, abstractmethod

from domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def create(
        self, ref_id: int | None, email: str, password: str
    ) -> User: ...

    @abstractmethod
    async def find_by_id(self, id: int) -> User | None: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def find_all_by_ref(self, ref: int) -> list[User]: ...
