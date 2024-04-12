from topic_lake_api.domain.interfaces.repositories import ITopicsRepository
from topic_lake_api.interactor.use_cases.base import UseCase


class ListTopics(UseCase):
    def __init__(self, repository: ITopicsRepository):
        self._repository = repository

    def execute(self):
        return self._repository.list()
