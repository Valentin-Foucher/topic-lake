from abc import abstractmethod, ABC

from topic_recommendations.interactor.dtos.outputs.items import ListItemsOutputDto, GetItemOutputDto
from topic_recommendations.interactor.interfaces.repositories.base import Repository


class IItemsRepository(Repository, ABC):
    @abstractmethod
    def list(self) -> ListItemsOutputDto:
        pass

    @abstractmethod
    def create(self, user_id: int, topic_id: int, content: str):
        pass

    @abstractmethod
    def get(self, item_id: int) -> GetItemOutputDto:
        pass

    @abstractmethod
    def delete(self, item_id: int):
        pass
