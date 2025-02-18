from sqlalchemy import select
from application.interfaces.user_repository import UserRepository
from domain.entities.user import User
from infrastructure.sql.repos.base import SQLRepositoryBase
from infrastructure.sql.models.user import SQLUser


class SQLUserRepository(SQLRepositoryBase, UserRepository):
    async def create(self, ref_id: int | None, email: str, password: str) -> User:
        u = SQLUser(ref=ref_id, email=email, password=password)
        self.session.add(u)
        await self.session.flush()
        return User.new(u.id, u.ref, u.email, u.password)

    async def find_by_id(self, id: int) -> User | None:
        u = await self.session.get(SQLUser, id)
        if u is None:
            return None
        return User.new(u.id, u.ref, u.email, u.password)

    async def find_by_email(self, email: str) -> User | None:
        u = await self.session.scalar(select(SQLUser).filter_by(email=email))
        if u is None:
            return None
        return User.new(u.id, u.ref, u.email, u.password)

    async def find_all_by_ref(self, ref: int) -> list[User]:
        us = await self.session.scalars(select(SQLUser).filter_by(ref=ref))
        return [User.new(u.id, u.ref, u.email, u.password) for u in us]
