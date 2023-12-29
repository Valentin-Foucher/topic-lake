from topic_recommendations.app.controllers.base import Controller
from topic_recommendations.app.presenters.users import GetUserPresenter
from topic_recommendations.interactor.interfaces.repositories.users import IUsersRepository
from topic_recommendations.interactor.use_cases.users.get_user import GetUser


class GetUserController(Controller):
    def __init__(self, presenter: GetUserPresenter, repository: IUsersRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self, user_id: int):
        return GetUser(self._presenter, self._repository).execute(user_id)

