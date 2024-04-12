from typing import Optional

from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.domain.interfaces.repositories import IAccessTokensRepository
from topic_lake_api.domain.interfaces.repositories import IUsersRepository
from topic_lake_api.use_cases.connection.logout import LogOut


class LogOutController(Controller):
    def __init__(self, access_tokens_repository: IAccessTokensRepository, users_repository: IUsersRepository):
        self._access_tokens_repository = access_tokens_repository
        self._users_repository = users_repository

    def execute(self, user_id: Optional[int]):
        return LogOut(self._access_tokens_repository, self._users_repository).execute(user_id)
