from abc import ABC, abstractmethod
from typing import Optional

from topic_recommendations.domain.entities.users import User
from topic_recommendations.interactor.interfaces.base import Repository


class IUsersRepository(Repository, ABC):
    @abstractmethod
    def create(self, name: str, hashed_password: str):
        pass

    @abstractmethod
    def get(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[User]:
        pass
