from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class CreateTopic(UseCase):
    def __init__(self, repository: ITopicsRepository):
        self._repository = repository

    def execute(self, user_id: int, content: str):
        self._repository.create(user_id, content)
