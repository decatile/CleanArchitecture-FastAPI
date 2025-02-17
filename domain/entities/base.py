from dataclasses import dataclass
from datetime import datetime

from utils.datetime import utc_now


@dataclass(frozen=True)
class NewType[V]:
    value: V


class ExpiresAt(NewType[datetime]):
    @property
    def expired(self):
        return self.value <= utc_now()
