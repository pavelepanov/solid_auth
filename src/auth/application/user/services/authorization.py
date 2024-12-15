from auth.application.ports.identity_provider import IdentityProvider
from auth.application.ports.user_data_gateway import UserDataGateway
from auth.application.user.errors import AuthorizationError
from auth.domain.user.entity import User
from auth.domain.user.enums import UserRoleEnum
from auth.domain.user.value_objects import UserId


class AuthorizationService:
    def __init__(
        self,
        idp: IdentityProvider,
        user_data_gateway: UserDataGateway,
    ):
        self._idp = idp
        self._user_data_gateway = user_data_gateway

    async def get_current_user_roles(self) -> set[UserRoleEnum]:
        current_user_id: UserId = await self._idp.get_current_user_id()

        user: User | None = await self._user_data_gateway.read_by_id(current_user_id)

        if user is None:
            raise AuthorizationError("Not authorized.")

        return user.roles

    async def check_authorization(self, role_required: UserRoleEnum) -> None:
        current_user_role: set[UserRoleEnum] = await self.get_current_user_roles()

        if role_required not in current_user_role:
            raise AuthorizationError("Not authorized.")
