from abc import abstractmethod


class SessionIdGenerator:
    @abstractmethod
    def __call__(self) -> str: ...
