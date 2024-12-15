from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from auth.domain.base.value_object import ValueObject


@dataclass(frozen=True, repr=False)
class SessionId(ValueObject):
    value: str


@dataclass(frozen=True, repr=False)
class UserId(ValueObject):
    value: UUID


@dataclass(frozen=True, repr=False)
class Expiration:
    value: datetime
