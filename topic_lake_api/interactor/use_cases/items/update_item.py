from topic_lake_api.interactor.exceptions import DoesNotExist
from topic_lake_api.interactor.interfaces.repositories.items import IItemsRepository
from topic_lake_api.interactor.use_cases.base import UseCase
from topic_lake_api.interactor.utils.item_utils import determine_rank


class UpdateItem(UseCase):
    def __init__(self, items_repository: IItemsRepository):
        self._items_repository = items_repository

    def execute(self, item_id: int, content: str, rank: int):
        item = self._items_repository.get(item_id)
        if not item:
            raise DoesNotExist(f'Item {item_id} does not exist')

        self._items_repository.update_ranks_for_topic(item.topic_id, rank)
        return self._items_repository.update(
            item_id,
            content,
            determine_rank(self._items_repository, rank, item.topic_id)
        )
