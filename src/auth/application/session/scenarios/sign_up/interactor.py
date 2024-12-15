from auth.application.enums import ResponseStatusEnum
from auth.application.ports.committer import Committer
from auth.application.ports.identity_provider import IdentityProvider
from auth.application.ports.user_data_gateway import UserDataGateway
from auth.application.session.errors import (
    AlreadyAuthenticatedError,
    AuthenticationError,
)
from auth.application.session.scenarios.sign_up.dtos import (
    SignUpRequest,
    SignUpResponse,
)
from auth.domain.user.entity import User
from auth.domain.user.errors.existence import UsernameAlreadyExists
from auth.domain.user.service import UserService
from auth.domain.user.value_objects import RawPassword, Username


class SignUp:
    def __init__(
        self,
        idp: IdentityProvider,
        user_data_gateway: UserDataGateway,
        user_service: UserService,
        committer: Committer,
    ):
        self._idp = idp
        self._user_data_gateway = user_data_gateway
        self._user_service = user_service
        self._committer = committer

    async def __call__(self, request_data: SignUpRequest) -> SignUpResponse:
        try:
            await self._idp.get_current_user_id()
            raise AlreadyAuthenticatedError(
                "You are already authenticated. Consider logging out."
            )
        except AuthenticationError:
            ...

        username: Username = Username(request_data.username)
        password: RawPassword = RawPassword(request_data.password)

        if not await self._user_data_gateway.is_username_unique(username):
            raise UsernameAlreadyExists(username.value)

        user: User = self._user_service.create_user(username, password)

        await self._user_data_gateway.save(user)
        await self._committer.commit()

        return SignUpResponse(user.username.value, ResponseStatusEnum.CREATED)
