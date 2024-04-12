from topic_lake_api.domain.entities import User
from topic_lake_api.domain.interfaces.repositories import IUsersRepository
from topic_lake_api.interactor.use_cases.base import UseCase


class CreateUser(UseCase):
    def __init__(self, repository: IUsersRepository):
        self._repository = repository

    def execute(self, name: str, password: str):
        return User.create(name,
                           password,
                           self._repository)
