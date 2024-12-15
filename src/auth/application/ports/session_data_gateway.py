from typing import Protocol
from abc import abstractmethod

from auth.domain.session.entity import Session
from auth.domain.session.value_objects import SessionId
from auth.domain.user.value_objects import UserId


class SessionDataGateway(Protocol):
    @abstractmethod
    def save(self, session: Session) -> None:
        raise NotImplementedError

    @abstractmethod
    def read(self, session_id: SessionId, for_update: bool) -> Session:
        raise NotImplementedError

    @abstractmethod
    def delete(self, session_id: SessionId) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete_all_for_user(self, user_id: UserId) -> None:
        raise NotImplementedError
