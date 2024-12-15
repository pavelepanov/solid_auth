from enum import Enum

from auth.infrastructure.sqla_persistence.tables.base import BaseDb
from auth.infrastructure.sqla_persistence.types.uuid_pk import uuidpk
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from sqlalchemy import TIMESTAMP, ForeignKey, String, LargeBinary, Enum
from datetime import datetime
from auth.domain.user.validation.constants import USERNAME_MAX_LEN
from auth.domain.user.enums import UserRoleEnum


class UserTable(BaseDb):
    __tablename__ = 'users'

    id: Mapped[uuidpk]
    username: Mapped[str] = mapped_column(String(USERNAME_MAX_LEN), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(LargeBinary, nullable=False)
    roles: Mapped[Enum] = mapped_column(Enum(UserRoleEnum), nullable=False, default=UserRoleEnum.USER)

    session: Mapped['SessionTable'] = relationship(back_populates='users')
