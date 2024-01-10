from topic_recommendations.interactor.exceptions import DoesNotExist
from topic_recommendations.interactor.interfaces.base import Presenter
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_recommendations.interactor.interfaces.repositories.users import IUsersRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class CreateItem(UseCase):
    def __init__(self, presenter: Presenter, items_repository: IItemsRepository, topics_repository: ITopicsRepository,
                 users_repository: IUsersRepository):
        self._presenter = presenter
        self._items_repository = items_repository
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    def execute(self, topic_id: int, user_id: int, content: str):
        if not self._users_repository.get(user_id):
            raise DoesNotExist(f'User {user_id} does not exist')

        if not self._topics_repository.get(topic_id):
            raise DoesNotExist(f'Topic {topic_id} does not exist')

        inserted_id = self._items_repository.create(topic_id, user_id, content)
        return self._presenter.present(inserted_id)


