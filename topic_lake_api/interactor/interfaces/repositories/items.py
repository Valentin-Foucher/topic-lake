from abc import abstractmethod, ABC

from topic_lake_api.domain.entities.items import Item
from topic_lake_api.interactor.interfaces.base import Repository


class IItemsRepository(Repository, ABC):
    @abstractmethod
    async def list(self, topic_id: int, limit: int = 100) -> list[Item]:
        pass

    @abstractmethod
    async def create(self, topic_id: int, user_id: int, content: str, rank: int) -> int:
        pass

    @abstractmethod
    async def get(self, item_id: int) -> Item:
        pass

    @abstractmethod
    async def delete(self, user_id: int, item_id: int) -> bool:
        pass

    @abstractmethod
    async def update(self, item_id: int, content: str, rank: int):
        pass

    @abstractmethod
    async def update_ranks_for_topic(self, topic_id: int, rank: int):
        pass

    @abstractmethod
    async def get_max_rank(self, topic_id: int) -> int:
        pass
