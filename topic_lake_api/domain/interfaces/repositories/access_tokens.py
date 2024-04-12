from abc import abstractmethod, ABC
from typing import Optional

from topic_lake_api.domain.interfaces.base import Repository


class IAccessTokensRepository(Repository, ABC):
    @abstractmethod
    def create(self, user_id: int) -> str:
        pass

    @abstractmethod
    def delete_all(self, user_id: int):
        pass

    @abstractmethod
    def get_latest(self, user_id: int) -> str:
        pass

    @abstractmethod
    def is_revoked(self, value: str) -> Optional[bool]:
        pass
