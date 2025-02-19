from dataclasses import dataclass
from typing import Optional, NewType


UserID = NewType("UserID", int)


Email = NewType("Email", str)


Password = NewType("Password", str)


@dataclass(frozen=True)
class User:
    id: UserID
    ref: Optional[UserID]
    email: Email
    password: Password

    @staticmethod
    def new(id: int, ref: int | None, email: str, password: str):
        return User(
            id=UserID(id),
            ref=UserID(ref) if ref is not None else None,
            email=Email(email),
            password=Password(password),
        )
