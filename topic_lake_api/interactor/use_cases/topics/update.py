from typing import Optional

from topic_lake_api.domain.interfaces.repositories import ITopicsRepository, IUsersRepository
from topic_lake_api.interactor.exceptions import DoesNotExist
from topic_lake_api.interactor.use_cases.base import UseCase


class UpdateTopic(UseCase):
    def __init__(self, topics_repository: ITopicsRepository, users_repository: IUsersRepository):
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    def execute(self, user_id: int, topic_id: int, parent_topic_id: Optional[int], content: str):
        topic = self._topics_repository.get(topic_id)
        if not topic:
            raise DoesNotExist(f'Topic {topic_id} does not exist')

        user = self._users_repository.get(user_id)
        if not user:
            raise DoesNotExist(f'User {user_id} does not exist')

        return topic.update(content, parent_topic_id, user_id, user.admin, self._topics_repository)
