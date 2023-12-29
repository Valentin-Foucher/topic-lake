from abc import ABC, abstractmethod

from topic_recommendations.domain.entities.topics import Topic
from topic_recommendations.interactor.interfaces.base import Repository


class ITopicsRepository(Repository, ABC):
    @abstractmethod
    def list(self, limit: int = 100) -> list[Topic]:
        pass

    @abstractmethod
    def create(self, user_id: int, content: str):
        pass

    @abstractmethod
    def get(self, topic_id: int) -> Topic:
        pass

    @abstractmethod
    def delete(self, topic_id: int):
        pass
