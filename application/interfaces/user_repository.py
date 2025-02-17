from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.user import User


@dataclass(frozen=True)
class UserCreateDTO:
    referral_code: str | None
    email: str
    password: str


class UserRepository(ABC):
    @abstractmethod
    async def create(self, model: UserCreateDTO) -> User: ...

    @abstractmethod
    async def find_by_id(self, id: int) -> User | None: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def find_all_by_ref(self, ref: int) -> list[User]: ...
