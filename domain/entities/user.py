from email_validator import EmailNotValidError, validate_email
from dataclasses import dataclass
from typing import Optional

from domain.entities.base import NewType
from domain.exceptions.validation import ValidationException


class UserID(NewType[int]): ...


class Email(NewType[str]):
    def __post_init__(self):
        try:
            validate_email(self.value)
        except EmailNotValidError:
            raise ValidationException()


class Password(NewType[str]): ...


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
