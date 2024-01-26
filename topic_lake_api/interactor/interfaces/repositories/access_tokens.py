from abc import abstractmethod, ABC
from typing import Optional

from topic_lake_api.interactor.interfaces.base import Repository


class IAccessTokensRepository(Repository, ABC):
    @abstractmethod
    async def create(self, user_id: int) -> str:
        pass

    @abstractmethod
    async def delete_all(self, user_id: int):
        pass

    @abstractmethod
    async def get_latest(self, user_id: int) -> str:
        pass

    @abstractmethod
    async def is_revoked(self, value: str) -> Optional[bool]:
        pass
