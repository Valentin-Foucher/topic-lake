from topic_recommendations.app.controllers.base import Controller
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_recommendations.interactor.use_cases.topics.create_topic import CreateTopic


class CreateTopicController(Controller):
    def __init__(self, repository: ITopicsRepository):
        self._repository = repository

    def execute(self, user_id: int, content: str):
        CreateTopic(self._repository).execute(user_id, content)

