from pydantic import BaseModel


class ReferralCodeCreateRequest(BaseModel):
    expires_in: int
