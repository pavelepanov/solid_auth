from sqlalchemy import Select, exists, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import eq

from auth.application.ports.user_data_gateway import UserDataGateway
from auth.domain.user.value_objects import UserId, Username
from auth.infrastructure.errors import DataMapperError
from auth.infrastructure.sqla_persistence.tables.user import UserTable


class SqlaUserDataMapper(UserDataGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, user: UserTable) -> None:
        try:
            self._session.add(user)
            await self._session.flush()

        except OSError as error:
            raise DataMapperError("Connection failed.") from error
        except SQLAlchemyError as error:
            raise DataMapperError("Database query failed.") from error

    async def read_by_id(self, user_id: UserId) -> UserTable | None:
        select_stmt: Select = select(UserTable).where(eq(UserTable.id_, user_id))  # type: ignore

        try:
            user: UserTable | None = (
                await self._session.execute(select_stmt)
            ).scalar_one_or_none()

            return user

        except OSError as error:
            raise DataMapperError("Connection failed.") from error
        except SQLAlchemyError as error:
            raise DataMapperError("Database query failed.") from error

    async def read_by_username(
        self, username: Username, for_update: bool = False
    ) -> UserTable | None:
        select_stmt: Select[tuple[UserTable]] = select(UserTable).where(
            eq(UserTable.username, username),  # type: ignore
        )

        if for_update:
            select_stmt = select_stmt.with_for_update()

        try:
            user: UserTable | None = (
                await self._session.execute(select_stmt)
            ).scalar_one_or_none()

            return user

        except OSError as error:
            raise DataMapperError("Connection failed.") from error
        except SQLAlchemyError as error:
            raise DataMapperError("Database query failed.") from error

    async def is_username_unique(self, username: Username) -> bool:
        select_exists_stmt: Select[tuple[bool]] = select(
            exists().where(eq(UserTable.username, username)),  # type: ignore
        )

        try:
            username_exists: bool = (
                await self._session.scalar(select_exists_stmt) or False
            )

            return not username_exists

        except OSError as error:
            raise DataMapperError("Connection failed.") from error
        except SQLAlchemyError as error:
            raise DataMapperError("Database query failed.") from error

    async def read_all(self, limit: int, offset: int) -> list[UserTable]:
        select_stmt: Select[tuple[UserTable]] = (
            select(UserTable).limit(limit).offset(offset)
        )

        try:
            users: list[UserTable] = list(
                (await self._session.scalars(select_stmt)).all()
            )

            return users

        except OSError as error:
            raise DataMapperError("Connection failed.") from error
        except SQLAlchemyError as error:
            raise DataMapperError("Database query failed.") from error
