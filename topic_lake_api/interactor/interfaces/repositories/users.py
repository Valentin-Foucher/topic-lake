from abc import ABC, abstractmethod
from typing import Optional

from topic_lake_api.domain.entities.users import User
from topic_lake_api.interactor.interfaces.base import Repository


class IUsersRepository(Repository, ABC):
    @abstractmethod
    async def create(self, name: str, hashed_password: str) -> int:
        pass

    @abstractmethod
    async def get(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[User]:
        pass
