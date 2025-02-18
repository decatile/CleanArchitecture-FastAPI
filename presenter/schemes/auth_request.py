from pydantic import BaseModel

from presenter.schemes.base import Email


class AuthRequest(BaseModel):
    email: Email
    password: str
