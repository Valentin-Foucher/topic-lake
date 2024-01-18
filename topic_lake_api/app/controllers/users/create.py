from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.app.presenters.users import CreateUserPresenter
from topic_lake_api.interactor.interfaces.repositories.users import IUsersRepository
from topic_lake_api.interactor.use_cases.users.create_user import CreateUser


class CreateUserController(Controller):
    def __init__(self, presenter: CreateUserPresenter, repository: IUsersRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self, name: str, password: str):
        result = CreateUser(self._repository).execute(name, password)
        return self._presenter.present(result)
