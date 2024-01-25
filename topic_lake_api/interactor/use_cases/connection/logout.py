from typing import Optional

from topic_lake_api.interactor.exceptions import DoesNotExist
from topic_lake_api.interactor.interfaces.repositories.access_tokens import IAccessTokensRepository
from topic_lake_api.interactor.interfaces.repositories.users import IUsersRepository
from topic_lake_api.interactor.use_cases.base import UseCase


class LogOut(UseCase):
    def __init__(self, access_tokens_repository: IAccessTokensRepository, users_repository: IUsersRepository):
        self._access_tokens_repository = access_tokens_repository
        self._users_repository = users_repository

    def execute(self, user_id: Optional[int]):
        if not user_id:
            return
        if not self._users_repository.get(user_id):
            raise DoesNotExist(f'User {user_id} does not exist')

        self._access_tokens_repository.delete_all(user_id)
