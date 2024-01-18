from typing import Optional

from topic_lake_api.interactor.exceptions import DoesNotExist
from topic_lake_api.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_lake_api.interactor.interfaces.repositories.users import IUsersRepository
from topic_lake_api.interactor.use_cases.base import UseCase


class CreateTopic(UseCase):
    def __init__(self, topics_repository: ITopicsRepository, users_repository: IUsersRepository):
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    def execute(self, user_id: int, parent_topic_id: Optional[int], content: str):
        if not self._users_repository.get(user_id):
            raise DoesNotExist(f'User {user_id} does not exist')
        
        if parent_topic_id:
            if not self._topics_repository.get(parent_topic_id):
                raise DoesNotExist(f'Topic {parent_topic_id} does not exist')

        return self._topics_repository.create(user_id, parent_topic_id, content)
