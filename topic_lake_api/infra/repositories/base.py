from abc import ABC
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession


class SQLRepository(ABC):
    _db: Optional[AsyncSession]

    def with_session(self, db: AsyncSession) -> 'SQLRepository':
        self._db = db
        return self
