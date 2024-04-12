from typing import Optional

from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.domain.interfaces.repositories import ITopicsRepository, IUsersRepository
from topic_lake_api.use_cases.topics.update import UpdateTopic


class UpdateTopicController(Controller):
    def __init__(self, topics_repository: ITopicsRepository, users_repository: IUsersRepository):
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    def execute(self, user_id: int, topic_id: int, parent_topic_id: Optional[int], content: str):
        UpdateTopic(self._topics_repository, self._users_repository).execute(
            user_id,
            topic_id,
            parent_topic_id,
            content
        )

