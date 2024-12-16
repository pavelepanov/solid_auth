from typing import Any, cast

import jwt

from auth.application.session.timer_utc import UtcSessionTimer
from auth.application.session.types import JwtAlgorithm, JwtSecret


class JwtAccessTokenProcessor:
    def __init__(
        self,
        secret: JwtSecret,
        algorithm: JwtAlgorithm,
        utc_session_timer: UtcSessionTimer,
    ):
        self._secret = secret
        self._algorithm = algorithm
        self._utc_session_timer = utc_session_timer

    def issue_access_token(self, session_id: str) -> str:
        to_encode: dict[str, Any] = {
            "session_id": session_id,
            "exp": int(self._utc_session_timer.access_expiration.timestamp()),
        }

        return jwt.encode(
            payload=to_encode,
            key=self._secret,
            algorithm=self._algorithm,
        )

    def extract_session_id(self, access_token: str) -> str | None:
        payload: dict[str, Any] | None = self._decode_token(access_token)

        if payload is None:
            return None

        session_id: str | None = payload.get("session_id")

        if session_id is None:
            return None

        return session_id

    def _decode_token(self, token: str) -> dict[str, Any] | None:
        try:
            return cast(
                dict[str, Any],
                jwt.decode(
                    jwt=token,
                    key=self._secret,
                    algorithms=[self._algorithm],
                ),
            )

        except jwt.PyJWTError:
            return None
