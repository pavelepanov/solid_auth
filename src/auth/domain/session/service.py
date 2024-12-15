from auth.domain.session.entity import Session
from auth.domain.session.ports.session_id_generator import SessionIdGenerator
from auth.domain.session.value_objects import Expiration, SessionId, UserId


class SessionService:
    def __init__(self, session_id_generator: SessionIdGenerator) -> None:
        self.session_id_generator = session_id_generator

    def create_session(self, user_id: UserId, expiration: Expiration) -> Session:
        session_id: SessionId = SessionId(self.session_id_generator())

        return Session(
            id_=session_id,
            user_id=user_id,
            expiration=expiration,
        )
