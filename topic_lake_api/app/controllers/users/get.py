from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.app.presenters.users import GetUserPresenter
from topic_lake_api.domain.interfaces.repositories import IUsersRepository
from topic_lake_api.interactor.use_cases.users.get import GetUser


class GetUserController(Controller):
    def __init__(self, presenter: GetUserPresenter, repository: IUsersRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self, user_id: int):
        result = GetUser(self._repository).execute(user_id)
        return self._presenter.present(result)

