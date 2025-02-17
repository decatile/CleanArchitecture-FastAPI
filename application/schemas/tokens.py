from dataclasses import dataclass


@dataclass(frozen=True)
class RefreshTokenResponseDTO:
    user_id: int
    refresh_token: str
    expires_in: int
