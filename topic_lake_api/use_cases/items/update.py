from topic_lake_api.domain.exceptions import DoesNotExist
from topic_lake_api.domain.interfaces.repositories import IItemsRepository
from topic_lake_api.use_cases.base import UseCase


class UpdateItem(UseCase):
    def __init__(self, items_repository: IItemsRepository):
        self._items_repository = items_repository

    def execute(self, item_id: int, content: str, rank: int):
        item = self._items_repository.get(item_id)
        if not item:
            raise DoesNotExist(f'Item {item_id} does not exist')

        return item.update(content, rank, self._items_repository)
