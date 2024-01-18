from abc import abstractmethod, ABC

from topic_recommendations.domain.entities.items import Item
from topic_recommendations.interactor.interfaces.base import Repository


class IItemsRepository(Repository, ABC):
    @abstractmethod
    def list(self, topic_id: int, limit: int = 100) -> list[Item]:
        pass

    @abstractmethod
    def create(self, topic_id: int, user_id: int, content: str, rank: int) -> int:
        pass

    @abstractmethod
    def get(self, item_id: int) -> Item:
        pass

    @abstractmethod
    def delete(self, item_id: int):
        pass

    @abstractmethod
    def update_ranks_for_topic(self, topic_id: int, rank: int):
        pass

    @abstractmethod
    def get_max_rank(self, topic_id: int) -> int:
        pass
