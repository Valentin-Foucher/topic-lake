from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class DeleteTopic(UseCase):
    def __init__(self, repository: ITopicsRepository):
        self._repository = repository

    def execute(self, topic_id: int):
        self._repository.delete(topic_id)
