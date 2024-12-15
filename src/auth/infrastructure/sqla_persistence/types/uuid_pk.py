from typing import Annotated

from sqlalchemy.orm import mapped_column
from uuid import UUID

uuidpk = Annotated[UUID, mapped_column(primary_key=True)]