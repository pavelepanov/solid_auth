from auth.infrastructure.sqla_persistence.tables.base import BaseDb
from auth.infrastructure.sqla_persistence.types.uuid_pk import uuidpk
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from sqlalchemy import TIMESTAMP, ForeignKey
from datetime import datetime


class SessionTable(BaseDb):
    __tablename__ = 'sessions'

    id: Mapped[uuidpk]
    expiration: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))

    user: Mapped['UserTable'] = relationship(back_populates='sessions')
