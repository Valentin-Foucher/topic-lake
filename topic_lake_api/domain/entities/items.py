from dataclasses import dataclass

from topic_lake_api.domain.entities.base import Entity
from topic_lake_api.domain.exceptions import DoesNotExist, InvalidInputData
from topic_lake_api.domain.interfaces.repositories import IUsersRepository, ITopicsRepository, IItemsRepository
from topic_lake_api.domain.utils.item_utils import determine_rank


@dataclass
class Item(Entity):
    id: int
    content: str
    topic_content: str
    topic_id: int
    user_name: str
    user_id: int
    rank: int

    @classmethod
    def create(cls,
               user_id: int,
               topic_id: int,
               content: str,
               rank: int,
               users_repository: IUsersRepository,
               topics_repository: ITopicsRepository,
               items_repository: IItemsRepository):

        if not users_repository.get(user_id):
            raise DoesNotExist(f'User {user_id} does not exist')

        if not topics_repository.get(topic_id):
            raise DoesNotExist(f'Topic {topic_id} does not exist')

        if items_repository.exists(topic_id, content):
            raise InvalidInputData('This item already exists')

        items_repository.update_ranks_for_topic(topic_id, rank)
        return items_repository.create(
            topic_id,
            user_id,
            content,
            determine_rank(items_repository, rank, topic_id)
        )

    def update(self, content: str, rank: int, items_repository: IItemsRepository):
        if content != self.content and items_repository.exists(self.topic_id, content):
            raise InvalidInputData('Cannot rename this item, a similar item already exists')

        if rank != self.rank:
            rank = determine_rank(items_repository, rank, self.topic_id)
            items_repository.update_ranks_for_topic(self.topic_id, rank, previous_rank=self.rank)

        return items_repository.update(
            self.id,
            content,
            rank
        )