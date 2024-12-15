from abc import abstractmethod
from typing import Protocol

from auth.domain.user.entity import User
from auth.domain.user.value_objects import UserId, Username


class UserDataGateway(Protocol):
    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def read_by_id(self, user_id: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def read_by_username(
        self, username: Username, for_update: bool = False
    ) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def is_username_unique(self, username: Username) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def read_all(self, limit: int, offset: int) -> list[User]:
        raise NotImplementedError
