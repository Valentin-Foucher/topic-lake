from topic_lake_api.domain.entities import Item
from topic_lake_api.domain.interfaces.repositories import IItemsRepository, ITopicsRepository, IUsersRepository
from topic_lake_api.use_cases.base import UseCase


class CreateItem(UseCase):
    def __init__(self, items_repository: IItemsRepository, topics_repository: ITopicsRepository,
                 users_repository: IUsersRepository):
        self._items_repository = items_repository
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    def execute(self, topic_id: int, user_id: int, content: str, rank: int):
        return Item.create(
            user_id,
            topic_id,
            content,
            rank,
            self._users_repository,
            self._topics_repository,
            self._items_repository
        )
