from topic_lake_api.domain.exceptions import InvalidInputData
from topic_lake_api.domain.interfaces.repositories import IAccessTokensRepository
from topic_lake_api.domain.interfaces.repositories import IUsersRepository
from topic_lake_api.domain.utils.encryption_utils import check_password
from topic_lake_api.use_cases.base import UseCase


class LogIn(UseCase):
    def __init__(self, access_tokens_repository: IAccessTokensRepository, users_repository: IUsersRepository):
        self._access_tokens_repository = access_tokens_repository
        self._users_repository = users_repository

    def execute(self, name: str, password: str):
        user = self._users_repository.get_by_name(name)
        if not (user and check_password(user.password, password)):
            raise InvalidInputData('Invalid credentials')

        return (
            self._access_tokens_repository.get_latest(user.id) or
            self._access_tokens_repository.create(user.id),
            user.id
        )
