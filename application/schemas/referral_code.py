from dataclasses import dataclass


@dataclass(frozen=True)
class ReferralCodeResponseDTO:
    code: str
