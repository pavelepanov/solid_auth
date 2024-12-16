from auth.application.ports.access_token_request_handler import (
    AccessTokenRequestHandler,
)
from auth.application.session.access_token_processor_jwt import JwtAccessTokenProcessor


class JwtTokenService:
    def __init__(
        self,
        jwt_access_token_processor: JwtAccessTokenProcessor,
        access_token_request_handler: AccessTokenRequestHandler,
    ):
        self._jwt_access_token_processor = jwt_access_token_processor
        self._access_token_request_handler = access_token_request_handler

    def issue_access_token(self, session_id: str) -> str:

        access_token: str = self._jwt_access_token_processor.issue_access_token(
            session_id
        )

        return access_token

    def add_access_token_to_request(self, access_token: str) -> None:

        self._access_token_request_handler.add_access_token_to_request(access_token)

    def delete_access_token_from_request(self) -> None:

        self._access_token_request_handler.delete_access_token_from_request()

    def get_access_token_from_request(self) -> str | None:

        access_token: str | None = (
            self._access_token_request_handler.get_access_token_from_request()
        )
        if not access_token:
            return None

        return access_token

    def get_session_id_from_access_token(self, access_token: str) -> str | None:

        session_id: str | None = self._jwt_access_token_processor.extract_session_id(
            access_token
        )
        if session_id is None:
            return None

        return session_id
