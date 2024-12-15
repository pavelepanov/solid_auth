from dataclasses import dataclass
from uuid import UUID

from auth.domain.base.value_object import ValueObject
from auth.domain.user.validation.validators import (
    validate_password_length,
    validate_username_length,
    validate_username_pattern,
)


@dataclass(frozen=True, repr=False)
class UserId(ValueObject):
    value: UUID


@dataclass(frozen=True, repr=False)
class Username(ValueObject):
    value: str

    def __post_init__(self) -> None:
        super().__post_init__()

        validate_username_length(self.value)
        validate_username_pattern(self.value)


@dataclass(frozen=True, repr=False)
class UserPasswordHash(ValueObject):
    value: bytes


@dataclass(frozen=True, repr=False)
class RawPassword(ValueObject):
    value: str

    def __post_init__(self) -> None:
        super().__post_init__()

        validate_password_length(self.value)
