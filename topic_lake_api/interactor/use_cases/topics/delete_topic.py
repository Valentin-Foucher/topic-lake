from topic_lake_api.domain.entities import Topic
from topic_lake_api.exceptions import InternalException
from topic_lake_api.interactor.exceptions import DoesNotExist, ForbiddenAction
from topic_lake_api.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_lake_api.interactor.interfaces.repositories.users import IUsersRepository
from topic_lake_api.interactor.use_cases.base import UseCase


class DeleteTopic(UseCase):
    def __init__(self, topics_repository: ITopicsRepository, users_repository: IUsersRepository):
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    async def execute(self, user_id: int, topic_id: int):
        topic = await self._topics_repository.get(topic_id)
        user = await self._users_repository.get(user_id)

        if not topic:
            raise DoesNotExist(f'Topic {topic_id} does not exist')
        if not user:
            raise DoesNotExist(f'User {user_id} does not exist')
        if not (user.admin or self.is_topic_entirely_owned(topic, user_id)):
            raise ForbiddenAction(f'This topic hierarchy was not entirely created by user {user_id}')

        result = await self._topics_repository.delete(user_id, topic_id)
        if not result:
            raise InternalException(f'Topic {topic_id} should have been deleted')

    def is_topic_entirely_owned(self, topic: Topic, user_id: int):
        return topic.user_id == user_id and \
            all(self.is_topic_entirely_owned(sub_topic, user_id) for sub_topic in topic.sub_topics if sub_topic)
