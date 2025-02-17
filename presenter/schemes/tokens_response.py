from pydantic import BaseModel


class TokensResponse(BaseModel):
    access_token: str
    expires_in: int
