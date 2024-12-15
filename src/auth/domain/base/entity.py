from abc import ABC
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from auth.domain.base.exceptions import DomainError
from auth.domain.base.value_object import ValueObject

T = TypeVar("T", bound=ValueObject)


@dataclass(eq=False)
class Entity(ABC, Generic[T]):
    id_: T

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "id_" and getattr(self, "id_", None) is not None:
            raise DomainError("Changing entity id is not permitted.")
        super().__setattr__(name, value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and other.id_ == self.id_

    def __hash__(self) -> int:
        return hash(self.id_)
