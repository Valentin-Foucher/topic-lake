from topic_lake_api.interactor.exceptions import DoesNotExist, InvalidInputData
from topic_lake_api.interactor.interfaces.repositories.access_tokens import IAccessTokensRepository
from topic_lake_api.interactor.interfaces.repositories.users import IUsersRepository
from topic_lake_api.interactor.use_cases.base import UseCase
from topic_lake_api.interactor.utils.encryption_utils import check_password


class LogIn(UseCase):
    def __init__(self, access_tokens_repository: IAccessTokensRepository, users_repository: IUsersRepository):
        self._access_tokens_repository = access_tokens_repository
        self._users_repository = users_repository

    def execute(self, name: str, password: str):
        user = self._users_repository.get_by_name(name)
        if not user:
            raise DoesNotExist(f'User "{name}" does not exist')

        if not check_password(user.password, password):
            raise InvalidInputData('Password is incorrect')

        return \
            self._access_tokens_repository.get_latest(user.id) or \
            self._access_tokens_repository.create(user.id)
