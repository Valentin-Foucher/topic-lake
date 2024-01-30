from abc import ABC

from sqlalchemy.orm import Session


class SQLRepository(ABC):
    def __init__(self):
        self._session = None

    def with_session(self, session: Session) -> 'SQLRepository':
        self._session = session
        return self
