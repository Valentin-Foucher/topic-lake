from topic_recommendations.app.controllers.base import Controller
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_recommendations.interactor.use_cases.topics.delete_topic import DeleteTopic


class DeleteTopicController(Controller):
    def __init__(self, repository: ITopicsRepository):
        self._repository = repository

    def execute(self, user_id: int, topic_id: int):
        DeleteTopic(self._repository).execute(
            user_id,
            topic_id
        )
