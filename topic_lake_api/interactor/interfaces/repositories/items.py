from abc import abstractmethod, ABC
from typing import Optional

from topic_lake_api.domain.entities.items import Item
from topic_lake_api.interactor.interfaces.base import Repository


class IItemsRepository(Repository, ABC):
    @abstractmethod
    def list(self, topic_id: int, limit: int = 100) -> list[Item]:
        pass

    @abstractmethod
    def create(self, topic_id: int, user_id: int, content: str, rank: int) -> int:
        pass

    @abstractmethod
    def get(self, item_id: int) -> Optional[Item]:
        pass

    @abstractmethod
    def delete(self, user_id: int, item_id: int) -> bool:
        pass

    @abstractmethod
    def update(self, item_id: int, content: str, rank: int):
        pass

    @abstractmethod
    def update_ranks_for_topic(self, topic_id: int, new_rank: int, previous_rank: int):
        pass

    @abstractmethod
    def get_max_rank(self, topic_id: int) -> int:
        pass
