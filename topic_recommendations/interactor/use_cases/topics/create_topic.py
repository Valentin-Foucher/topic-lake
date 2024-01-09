from topic_recommendations.interactor.exceptions import DoesNotExist
from topic_recommendations.interactor.interfaces.base import Presenter
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_recommendations.interactor.interfaces.repositories.users import IUsersRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class CreateTopic(UseCase):
    def __init__(self, presenter: Presenter, topics_repository: ITopicsRepository, users_repository: IUsersRepository):
        self._presenter = presenter
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    def execute(self, user_id: int, content: str):
        if not self._users_repository.get(user_id):
            raise DoesNotExist(f'User {user_id} does not exist')

        inserted_id = self._topics_repository.create(user_id, content)
        return self._presenter.present(inserted_id)
