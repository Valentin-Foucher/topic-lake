from abc import ABC, abstractmethod
from typing import Optional

from topic_lake_api.domain.entities.topics import Topic
from topic_lake_api.interactor.interfaces.base import Repository


class ITopicsRepository(Repository, ABC):
    @abstractmethod
    async def list(self, limit: int = 100) -> list[Topic]:
        pass

    @abstractmethod
    async def create(self, user_id: int, parent_topic_id: Optional[int], content: str):
        pass

    @abstractmethod
    async def get(self, topic_id: int) -> Topic:
        pass

    @abstractmethod
    async def delete(self, user_id: int, topic_id: int) -> bool:
        pass

    @abstractmethod
    async def update(self, user_id: int, topic_id: int, parent_topic_id: Optional[int], content: str):
        pass

    @abstractmethod
    async def exists(self, parent_topic_id: Optional[int], content: str) -> bool:
        pass
