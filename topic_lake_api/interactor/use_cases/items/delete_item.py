from topic_lake_api.interactor.exceptions import DoesNotExist
from topic_lake_api.interactor.interfaces.repositories.items import IItemsRepository
from topic_lake_api.interactor.use_cases.base import UseCase


class DeleteItem(UseCase):
    def __init__(self, repository: IItemsRepository):
        self._repository = repository

    async def execute(self, user_id: int, item_id: int):
        result = await self._repository.delete(user_id, item_id)
        if not result:
            raise DoesNotExist(f'Item {item_id} does not exist')
