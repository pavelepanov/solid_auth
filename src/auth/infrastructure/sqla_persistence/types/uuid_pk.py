from typing import Annotated
from uuid import UUID

from sqlalchemy.orm import mapped_column

uuidpk = Annotated[UUID, mapped_column(primary_key=True)]
