import sys
from typing import Optional

from sqlalchemy import select, update, and_, func, or_, delete
from sqlalchemy.exc import NoResultFound

from topic_lake_api.domain.entities.items import Item
from topic_lake_api.infra.db.models import Item as ItemModel
from topic_lake_api.infra.db.models import User as UserModel
from topic_lake_api.infra.repositories.base import SQLRepository
from topic_lake_api.interactor.interfaces.repositories.items import IItemsRepository


class ItemsRepository(SQLRepository, IItemsRepository):
    def list(self, topic_id: int, limit: int = 100) -> list[Item]:
        item_list = self._session.scalars(
            select(ItemModel)
            .where(ItemModel.topic_id == topic_id)
            .order_by(ItemModel.rank)
            .limit(limit)
        ).all()
        return [item.as_dataclass() for item in item_list]

    def create(self, topic_id: int,  user_id: int, content: str, rank: int) -> int:
        i = ItemModel(topic_id=topic_id,
                      user_id=user_id,
                      content=content,
                      rank=rank)
        self._session.add(i)
        self._session.flush()

        return i.id

    def get(self, item_id: int) -> Optional[Item]:
        try:
            item = self._session.scalars(
                select(ItemModel)
                .where(ItemModel.id == item_id)
                .limit(1)
            ).one()
        except NoResultFound:
            return None

        return item.as_dataclass()

    def delete(self, user_id: int, item_id: int) -> bool:
        deleted_rows = \
            self._session.execute(
                delete(ItemModel).filter(
                    and_(
                        ItemModel.id == item_id,
                        or_(
                            UserModel.admin.is_(True),
                            ItemModel.user_id == user_id
                        )
                    )
                ).returning(ItemModel.id)
            ).fetchall()

        result = len(deleted_rows) != 0
        return result

    def update(self, item_id: int, content: str, rank: int):
        self._session.execute(
            update(ItemModel)
            .filter(ItemModel.id == item_id)
            .values(content=content, rank=rank)
        )

    def update_ranks_for_topic(self, topic_id: int, new_rank: int, previous_rank: int = sys.maxsize):
        if previous_rank < new_rank:
            self._session.execute(
                update(ItemModel)
                .where(
                    and_(
                        ItemModel.topic_id == topic_id,
                        ItemModel.rank > previous_rank,
                        ItemModel.rank <= new_rank
                    )
                )
                .values(rank=ItemModel.rank - 1)
            )

        self._session.execute(
            update(ItemModel)
            .where(
                and_(
                    ItemModel.topic_id == topic_id,
                    ItemModel.rank < previous_rank,
                    ItemModel.rank >= new_rank
                )
            )
            .values(rank=ItemModel.rank + 1)
        )

    def get_max_rank(self, topic_id: int) -> int:
        return self._session.scalars(
            select(func.max(ItemModel.rank))
            .where(ItemModel.topic_id == topic_id)
            .limit(1)
        ).one() or 0

    def exists(self, topic_id: int, content: str) -> bool:
        try:
            self._session.scalars(
                select(ItemModel)
                .where(
                    and_(
                        ItemModel.topic_id == topic_id,
                        func.lower(ItemModel.content) == content.lower(),
                    )
                ).limit(1)
            ).one()
        except NoResultFound:
            return False

        return True
