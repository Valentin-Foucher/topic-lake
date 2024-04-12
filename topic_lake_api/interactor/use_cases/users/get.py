from topic_lake_api.domain.interfaces.repositories import IUsersRepository
from topic_lake_api.interactor.exceptions import DoesNotExist
from topic_lake_api.interactor.use_cases.base import UseCase


class GetUser(UseCase):
    def __init__(self, repository: IUsersRepository):
        self._repository = repository

    def execute(self, user_id: int):
        result = self._repository.get(user_id)
        if not result:
            raise DoesNotExist(f'User {user_id} does not exist')
        return result
