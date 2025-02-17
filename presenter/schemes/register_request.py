from pydantic import BaseModel


class RegisterRequest(BaseModel):
    referral_code: str | None
    email: str
    password: str
