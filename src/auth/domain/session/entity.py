from dataclasses import dataclass

from auth.domain.base.entity import Entity
from auth.domain.session.value_objects import Expiration, SessionId, UserId


@dataclass(eq=False, kw_only=True)
class Session(Entity[SessionId]):
    user_id: UserId
    expiration: Expiration
