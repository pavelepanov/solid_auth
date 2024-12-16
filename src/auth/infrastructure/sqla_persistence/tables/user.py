from sqlalchemy import Enum, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth.domain.user.enums import UserRoleEnum
from auth.domain.user.validation.constants import USERNAME_MAX_LEN
from auth.infrastructure.sqla_persistence.tables.base import BaseDb
from auth.infrastructure.sqla_persistence.types.uuid_pk import uuidpk


class UserTable(BaseDb):
    __tablename__ = "users"

    id: Mapped[uuidpk]
    username: Mapped[str] = mapped_column(
        String(USERNAME_MAX_LEN), nullable=False, unique=True
    )
    password_hash: Mapped[str] = mapped_column(LargeBinary, nullable=False)
    roles: Mapped[Enum] = mapped_column(
        Enum(UserRoleEnum), nullable=False, default=UserRoleEnum.USER
    )

    session: Mapped["SessionTable"] = relationship(back_populates="users")
