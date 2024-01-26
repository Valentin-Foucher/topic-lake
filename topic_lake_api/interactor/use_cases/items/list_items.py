from topic_lake_api.interactor.interfaces.repositories.items import IItemsRepository
from topic_lake_api.interactor.use_cases.base import UseCase


class ListItems(UseCase):
    def __init__(self, repository: IItemsRepository):
        self._repository = repository

    async def execute(self, topic_id: int):
        return await self._repository.list(topic_id)
