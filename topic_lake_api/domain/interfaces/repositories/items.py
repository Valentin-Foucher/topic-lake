import sys
from abc import abstractmethod, ABC
from typing import Optional, TYPE_CHECKING

from topic_lake_api.domain.interfaces.base import Repository

if TYPE_CHECKING:
    from topic_lake_api.domain.entities import Item


class IItemsRepository(Repository, ABC):
    @abstractmethod
    def list(self, topic_id: int, limit: int = 100) -> list['Item']:
        pass

    @abstractmethod
    def create(self, topic_id: int, user_id: int, content: str, rank: int) -> int:
        pass

    @abstractmethod
    def get(self, item_id: int) -> Optional['Item']:
        pass

    @abstractmethod
    def delete(self, user_id: int, item_id: int) -> bool:
        pass

    @abstractmethod
    def update(self, item_id: int, content: str, rank: int):
        pass

    @abstractmethod
    def update_ranks_for_topic(self, topic_id: int, new_rank: int, previous_rank: int = sys.maxsize):
        pass

    @abstractmethod
    def get_max_rank(self, topic_id: int) -> int:
        pass

    @abstractmethod
    def exists(self, topic_id: int, content: str) -> bool:
        pass
