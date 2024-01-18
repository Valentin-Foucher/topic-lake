from topic_lake_api.interactor.exceptions import DoesNotExist
from topic_lake_api.interactor.interfaces.repositories.items import IItemsRepository
from topic_lake_api.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_lake_api.interactor.interfaces.repositories.users import IUsersRepository
from topic_lake_api.interactor.use_cases.base import UseCase


class CreateItem(UseCase):
    def __init__(self, items_repository: IItemsRepository, topics_repository: ITopicsRepository,
                 users_repository: IUsersRepository):
        self._items_repository = items_repository
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    def execute(self, topic_id: int, user_id: int, content: str, rank: int):
        if not self._users_repository.get(user_id):
            raise DoesNotExist(f'User {user_id} does not exist')

        if not self._topics_repository.get(topic_id):
            raise DoesNotExist(f'Topic {topic_id} does not exist')

        self._items_repository.update_ranks_for_topic(topic_id, rank)
        max_rank = self._items_repository.get_max_rank(topic_id)

        return self._items_repository.create(topic_id, user_id, content, min(rank, max_rank + 1))
