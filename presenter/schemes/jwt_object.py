from dataclasses import dataclass


@dataclass(frozen=True)
class JwtObject:
    user_id: int
