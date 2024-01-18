from topic_lake_api.interactor.exceptions import DoesNotExist
from topic_lake_api.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_lake_api.interactor.use_cases.base import UseCase


class DeleteTopic(UseCase):
    def __init__(self, repository: ITopicsRepository):
        self._repository = repository

    def execute(self, user_id: int, topic_id: int):
        result = self._repository.delete(user_id, topic_id)
        if not result:
            raise DoesNotExist(f'Topic {topic_id} does not exist')
