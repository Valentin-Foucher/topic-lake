from topic_recommendations.interactor.exceptions import DoesNotExist
from topic_recommendations.interactor.interfaces.base import Presenter
from topic_recommendations.interactor.interfaces.repositories.users import IUsersRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class GetUser(UseCase):
    def __init__(self, presenter: Presenter, repository: IUsersRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self, user_id: int):
        result = self._repository.get(user_id)
        if not result:
            raise DoesNotExist(f'User {user_id} does not exist')
        return self._presenter.present(result)
