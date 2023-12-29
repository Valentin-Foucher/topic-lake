from topic_recommendations.app.controllers.base import Controller
from topic_recommendations.interactor.interfaces.repositories.users import IUsersRepository
from topic_recommendations.interactor.use_cases.users.create_user import CreateUser


class CreateUserController(Controller):
    def __init__(self, repository: IUsersRepository):
        self._repository = repository

    def execute(self, name: str, password: str):
        CreateUser(self._repository).execute(name, password)

