from topic_lake_api.domain.exceptions import DoesNotExist
from topic_lake_api.domain.interfaces.repositories import ITopicsRepository, IUsersRepository
from topic_lake_api.use_cases.base import UseCase


class DeleteTopic(UseCase):
    def __init__(self, topics_repository: ITopicsRepository, users_repository: IUsersRepository):
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    def execute(self, user_id: int, topic_id: int):
        topic = self._topics_repository.get(topic_id)
        user = self._users_repository.get(user_id)

        if not topic:
            raise DoesNotExist(f'Topic {topic_id} does not exist')

        topic.delete(user, self._topics_repository)

