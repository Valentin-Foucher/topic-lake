from typing import Optional

from topic_lake_api.interactor.exceptions import DoesNotExist, ForbiddenAction, InvalidInputData
from topic_lake_api.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_lake_api.interactor.interfaces.repositories.users import IUsersRepository
from topic_lake_api.interactor.use_cases.base import UseCase


class UpdateTopic(UseCase):
    def __init__(self, topics_repository: ITopicsRepository, users_repository: IUsersRepository):
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    def execute(self, user_id: int, topic_id: int, parent_topic_id: Optional[int], content: str):
        if parent_topic_id and not self._topics_repository.get(parent_topic_id):
            raise DoesNotExist(f'Topic {parent_topic_id} does not exist')

        topic = self._topics_repository.get(topic_id)
        if not topic:
            raise DoesNotExist(f'Topic {topic_id} does not exist')

        user = self._users_repository.get(user_id)
        if topic.user_id != user_id and not user.admin:
            raise ForbiddenAction(f'This topic is not owned by user {user_id}')

        if self._topics_repository.exists(parent_topic_id, content):
            raise InvalidInputData('This topic already exists')

        return self._topics_repository.update(user_id, topic_id, parent_topic_id, content)
