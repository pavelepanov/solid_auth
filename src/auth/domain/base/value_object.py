from abc import ABC
from dataclasses import asdict, dataclass, fields
from typing import Any

from auth.domain.base.errors import DomainFieldError


@dataclass(frozen=True, repr=False)
class ValueObject(ABC):
    def __post_init__(self) -> None:
        if not fields(self):
            raise DomainFieldError(
                f"{type(self).__name__} must have at least one field!"
            )

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._repr_value()})"

    def _repr_value(self) -> str:
        all_fields = fields(self)
        if len(all_fields) == 1:
            return f"{getattr(self, all_fields[0].name)!r}"
        return ", ".join(f"{f.name}={getattr(self, f.name)!r}" for f in all_fields)

    def get_fields(self) -> dict[str, Any]:
        return asdict(self)
