from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.ports.committer import Committer
from auth.infrastructure.errors import DataMapperError


class SqlaCommitter(Committer):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        try:
            await self._session.commit()

        except OSError as error:
            raise DataMapperError("Connection failed, commit failed.") from error
        except SQLAlchemyError as error:
            raise DataMapperError("Database query failed, commit failed.") from error


