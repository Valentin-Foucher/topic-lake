from abc import ABC, abstractmethod
from typing import Optional, List

from topic_recommendations.domain.entities.topics import Topic
from topic_recommendations.interactor.interfaces.base import Repository


class ITopicsRepository(Repository, ABC):
    @abstractmethod
    def list(self, limit: int = 100) -> list[Topic]:
        pass

    @abstractmethod
    def create(self, user_id: int, parent_topic_id: Optional[int], content: str):
        pass

    @abstractmethod
    def get(self, topic_id: int) -> Topic:
        pass

    @abstractmethod
    def delete(self, topic_id: int):
        pass

    @abstractmethod
    def list_as_treeviews(self) -> List[Topic]:
        pass
