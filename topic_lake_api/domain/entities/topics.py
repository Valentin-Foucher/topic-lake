from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from typing_extensions import Self

from topic_lake_api.domain.interfaces.repositories import ITopicsRepository
from topic_lake_api.domain.interfaces.repositories import IUsersRepository
from topic_lake_api.exceptions import InternalException
from topic_lake_api.interactor.exceptions import ForbiddenAction, DoesNotExist, InvalidInputData

if TYPE_CHECKING:
    from topic_lake_api.domain.entities import User


@dataclass
class Topic:
    id: int
    content: str
    user_id: int
    parent_topic_id: Optional[int] = None
    sub_topics: list[Self] = field(default_factory=list)

    @classmethod
    def create(cls,
               user_id: int,
               content: str,
               parent_topic_id: int,
               users_repository: IUsersRepository,
               topics_repository: ITopicsRepository):

        if not users_repository.get(user_id):
            raise DoesNotExist(f'User {user_id} does not exist')

        if parent_topic_id and not topics_repository.get(parent_topic_id):
            raise DoesNotExist(f'Topic {parent_topic_id} does not exist')

        if topics_repository.exists(parent_topic_id, content):
            raise InvalidInputData('This topic already exists')

        return topics_repository.create(user_id, parent_topic_id, content)

    def update(self,
               content: str,
               parent_topic_id: int,
               user_id: int,
               is_user_admin: bool,
               topics_repository: ITopicsRepository):

        if parent_topic_id and not topics_repository.get(parent_topic_id):
            raise DoesNotExist(f'Topic {parent_topic_id} does not exist')

        if self.user_id != user_id and not is_user_admin:
            raise ForbiddenAction(f'This topic is not owned by user {user_id}')

        if topics_repository.exists(parent_topic_id, content):
            raise InvalidInputData('Cannot move or rename this topic, a similar topic already exists')

        return topics_repository.update(user_id, self.id, parent_topic_id, content)

    def delete(self, user: Optional['User'], topics_repository: ITopicsRepository):
        if not user:
            raise DoesNotExist(f'User {user.id} does not exist')

        if not (user.admin or self._is_topic_entirely_owned(self, user.id)):
            raise ForbiddenAction(f'This topic hierarchy was not entirely created by user {user.id}')

        result = topics_repository.delete(user.id, self.id)
        if not result:
            raise InternalException(f'Topic {self.id} should have been deleted')

    def _is_topic_entirely_owned(self, topic: Self, user_id: int) -> bool:
        return topic.user_id == user_id and \
            all(self._is_topic_entirely_owned(sub_topic, user_id) for sub_topic in topic.sub_topics if sub_topic)
