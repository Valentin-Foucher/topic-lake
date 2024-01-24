from typing import Optional

from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_lake_api.interactor.use_cases.topics.update_topic import UpdateTopic


class UpdateTopicController(Controller):
    def __init__(self, topics_repository: ITopicsRepository):
        self._topics_repository = topics_repository

    def execute(self, user_id: int, topic_id: int, parent_topic_id: Optional[int], content: str):
        UpdateTopic(self._topics_repository).execute(
            user_id,
            topic_id,
            parent_topic_id,
            content
        )

