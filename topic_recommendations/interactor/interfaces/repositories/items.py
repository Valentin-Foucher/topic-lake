from abc import abstractmethod, ABC

from topic_recommendations.domain.entities.items import Item
from topic_recommendations.interactor.interfaces.base import Repository


class IItemsRepository(Repository, ABC):
    @abstractmethod
    def list(self, limit: int = 100) -> list[Item]:
        pass

    @abstractmethod
    def create(self, user_id: int, topic_id: int, content: str):
        pass

    @abstractmethod
    def get(self, item_id: int) -> Item:
        pass

    @abstractmethod
    def delete(self, item_id: int):
        pass
