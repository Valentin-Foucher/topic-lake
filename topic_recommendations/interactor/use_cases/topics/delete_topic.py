from topic_recommendations.interactor.exceptions import DoesNotExist
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class DeleteTopic(UseCase):
    def __init__(self, repository: ITopicsRepository):
        self._repository = repository

    def execute(self, topic_id: int):
        result = self._repository.delete(topic_id)
        if not result:
            raise DoesNotExist(f'Topic {topic_id} does not exist')
