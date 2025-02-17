from pydantic import BaseModel


class CreateReferralResponse(BaseModel):
    code: str
