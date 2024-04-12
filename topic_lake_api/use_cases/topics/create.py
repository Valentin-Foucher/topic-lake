from typing import Optional

from topic_lake_api.domain.entities import Topic
from topic_lake_api.domain.interfaces.repositories import ITopicsRepository, IUsersRepository
from topic_lake_api.use_cases.base import UseCase


class CreateTopic(UseCase):
    def __init__(self, topics_repository: ITopicsRepository, users_repository: IUsersRepository):
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    def execute(self, user_id: int, parent_topic_id: Optional[int], content: str):
        return Topic.create(user_id,
                            content,
                            parent_topic_id,
                            self._users_repository,
                            self._topics_repository)
