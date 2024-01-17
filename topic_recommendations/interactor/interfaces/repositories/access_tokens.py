from abc import abstractmethod, ABC
from typing import Optional

from topic_recommendations.interactor.interfaces.base import Repository


class IAccessTokensRepository(Repository, ABC):
    @abstractmethod
    def create(self, user_id: int) -> str:
        pass

    @abstractmethod
    def delete_all(self, user_id: int):
        pass

    @abstractmethod
    def get_latest(self, user_id: int) -> str:
        pass

    @abstractmethod
    def get_user_id_for_value(self, value: str) -> Optional[int]:
        pass
