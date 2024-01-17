from topic_recommendations.app.controllers.base import Controller
from topic_recommendations.interactor.interfaces.base import Presenter
from topic_recommendations.interactor.interfaces.repositories.access_tokens import IAccessTokensRepository
from topic_recommendations.interactor.interfaces.repositories.users import IUsersRepository
from topic_recommendations.interactor.use_cases.connection.login import LogIn


class LogInController(Controller):
    def __init__(self, presenter: Presenter, access_tokens_repository: IAccessTokensRepository,
                 users_repository: IUsersRepository):
        self._presenter = presenter
        self._access_tokens_repository = access_tokens_repository
        self._users_repository = users_repository

    def execute(self, username: str, password: str):
        result = LogIn(self._access_tokens_repository, self._users_repository) \
            .execute(username, password)
        return self._presenter.present(result)
