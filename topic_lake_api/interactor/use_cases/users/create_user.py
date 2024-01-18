from topic_lake_api.interactor.exceptions import AlreadyExist
from topic_lake_api.interactor.interfaces.repositories.users import IUsersRepository
from topic_lake_api.interactor.use_cases.base import UseCase
from topic_lake_api.interactor.utils.encryption_utils import hash_password


class CreateUser(UseCase):
    def __init__(self, repository: IUsersRepository):
        self._repository = repository

    def execute(self, name: str, password: str):
        if self._repository.get_by_name(name):
            raise AlreadyExist(f'User "{name}" already exists')

        hashed_password = hash_password(password)
        return self._repository.create(name, hashed_password)
