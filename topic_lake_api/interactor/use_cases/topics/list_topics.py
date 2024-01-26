from topic_lake_api.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_lake_api.interactor.use_cases.base import UseCase


class ListTopics(UseCase):
    def __init__(self, repository: ITopicsRepository):
        self._repository = repository

    async def execute(self):
        return await self._repository.list()
