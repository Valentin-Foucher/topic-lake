from topic_recommendations.app.presenters.users import GetUserPresenter
from topic_recommendations.interactor.interfaces.repositories.users import IUsersRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class GetUser(UseCase):
    def __init__(self, presenter: GetUserPresenter, repository: IUsersRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self, user_id: int):
        result = self._repository.get(user_id)
        if not result:
            return None
        return self._presenter.present(result)
