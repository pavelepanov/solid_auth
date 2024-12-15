from sqlalchemy import Delete, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.dml import ReturningDelete
from sqlalchemy.sql.operators import eq

from auth.domain.user.value_objects import UserId
from auth.domain.session.entity import Session
from auth.infrastructure.errors import DataMapperError


class SqlaSessionDataMapper:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, session_record: Session) -> None:
        try:
            self._session.add(session_record)
            await self._session.flush()

        except OSError as error:
            raise DataMapperError("Connection failed.") from error
        except SQLAlchemyError as error:
            raise DataMapperError("Database query failed.") from error

    async def read(
        self, session_id: str, for_update: bool = False
    ) -> Session | None:
        try:
            session: Session | None = await self._session.get(
                Session,
                session_id,
                with_for_update=for_update,
            )

            return session

        except OSError as error:
            raise DataMapperError("Connection failed.") from error
        except SQLAlchemyError as error:
            raise DataMapperError("Database query failed.") from error

    async def delete(self, session_id: str) -> bool:
        delete_stmt: ReturningDelete[tuple[str, ...]] = (
            delete(Session)
            .where(eq(Session.id_, session_id))  # type: ignore
            .returning(Session.id_)
        )

        try:
            result = await self._session.execute(delete_stmt)
            await self._session.flush()
            deleted_ids: tuple[str, ...] = tuple(result.scalars().all())

            return bool(deleted_ids)

        except OSError as error:
            raise DataMapperError("Connection failed.") from error
        except SQLAlchemyError as error:
            raise DataMapperError("Database query failed.") from error

    async def delete_all_for_user(self, user_id: UserId) -> None:
        delete_stmt: Delete = delete(Session).where(
            eq(Session.user_id, user_id)  # type: ignore
        )

        try:
            await self._session.execute(delete_stmt)
            await self._session.flush()

        except OSError as error:
            raise DataMapperError("Connection failed.") from error
        except SQLAlchemyError as error:
            raise DataMapperError("Database query failed.") from error
