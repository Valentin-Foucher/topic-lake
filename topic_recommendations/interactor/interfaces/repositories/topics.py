from abc import ABC, abstractmethod

from topic_recommendations.interactor.dtos.outputs.topics import GetTopicOutputDto, ListTopicsOutputDto
from topic_recommendations.interactor.interfaces.repositories.base import Repository


class ITopicsRepository(Repository, ABC):
    @abstractmethod
    def list(self) -> ListTopicsOutputDto:
        pass

    @abstractmethod
    def create(self, user_id: int, content: str):
        pass

    @abstractmethod
    def get(self, topic_id: int) -> GetTopicOutputDto:
        pass

    @abstractmethod
    def delete(self, topic_id: int):
        pass
