from topic_lake_api.domain.exceptions import DoesNotExist
from topic_lake_api.domain.interfaces.repositories import ITopicsRepository
from topic_lake_api.use_cases.base import UseCase


class GetTopic(UseCase):
    def __init__(self, repository: ITopicsRepository):
        self._repository = repository

    def execute(self, topic_id: int):
        result = self._repository.get(topic_id)
        if not result:
            raise DoesNotExist(f'Topic {topic_id} does not exist')

        return result
