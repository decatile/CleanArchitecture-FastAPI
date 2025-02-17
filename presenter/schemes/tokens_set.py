from dataclasses import dataclass


@dataclass(frozen=True)
class TokensSet:
    access_token: str
    access_token_expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
