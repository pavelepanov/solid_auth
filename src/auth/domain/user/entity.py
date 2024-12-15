from dataclasses import dataclass

from app.domain.base.entity import Entity
from app.domain.user.enums import UserRoleEnum
from app.domain.user.value_objects import UserId, Username, UserPasswordHash


@dataclass(eq=False, kw_only=True)
class User(Entity[UserId]): ...
