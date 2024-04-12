from dataclasses import dataclass

from topic_lake_api.domain.interfaces.repositories import IUsersRepository
from topic_lake_api.interactor.exceptions import AlreadyExist
from topic_lake_api.interactor.utils.encryption_utils import hash_password


@dataclass
class User:
    id: int
    name: str
    password: str
    admin: bool

    @classmethod
    def create(cls, name: str, password: str, users_repository: IUsersRepository):
        if users_repository.get_by_name(name):
            raise AlreadyExist(f'User "{name}" already exists')

        hashed_password = hash_password(password)
        return users_repository.create(name, hashed_password)
