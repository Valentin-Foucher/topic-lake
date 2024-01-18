from topic_lake_api.interactor.exceptions import DoesNotExist
from topic_lake_api.interactor.interfaces.repositories.items import IItemsRepository
from topic_lake_api.interactor.use_cases.base import UseCase


class GetItem(UseCase):
    def __init__(self, repository: IItemsRepository):
        self._repository = repository

    def execute(self, item_id: int):
        result = self._repository.get(item_id)
        if not result:
            raise DoesNotExist(f'Item {item_id} does not exist')

        return result
