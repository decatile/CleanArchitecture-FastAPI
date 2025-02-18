from pydantic import BaseModel

from presenter.schemes.base import Email


class RegisterRequest(BaseModel):
    referral_code: str | None
    email: Email
    password: str
