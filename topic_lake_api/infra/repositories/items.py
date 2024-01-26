from typing import Optional

from sqlalchemy import select, update, and_, func, or_, delete
from sqlalchemy.exc import NoResultFound

from topic_lake_api.domain.entities.items import Item
from topic_lake_api.infra.db.models import Item as ItemModel
from topic_lake_api.infra.db.models import User as UserModel
from topic_lake_api.infra.repositories.base import SQLRepository
from topic_lake_api.interactor.interfaces.repositories.items import IItemsRepository


class ItemsRepository(SQLRepository, IItemsRepository):
    async def list(self, topic_id: int, limit: int = 100) -> list[Item]:
        item_list = (await self._db.scalars(
            select(ItemModel)
            .where(ItemModel.topic_id == topic_id)
            .order_by(ItemModel.id)
            .limit(limit)
        )).all()
        return [item.as_dataclass() for item in item_list]

    async def create(self, topic_id: int,  user_id: int, content: str, rank: int) -> int:
        i = ItemModel(topic_id=topic_id,
                      user_id=user_id,
                      content=content,
                      rank=rank)

        self._db.add(i)
        await self._db.commit()
        await self._db.flush()

        return i.id

    async def get(self, item_id: int) -> Optional[Item]:
        try:
            item = (await self._db.scalars(
                select(ItemModel)
                .where(ItemModel.id == item_id)
                .limit(1)
            )).one()
        except NoResultFound:
            return None

        return item.as_dataclass()

    async def delete(self, user_id: int, item_id: int) -> bool:
        deleted_rows = \
            (await self._db.execute(
                delete(ItemModel).filter(
                    and_(
                        ItemModel.id == item_id,
                        or_(
                            UserModel.admin.is_(True),
                            ItemModel.user_id == user_id
                        )
                    )
                ).returning(ItemModel.id)
            )).fetchall()

        result = len(deleted_rows) != 0
        await self._db.commit()
        return result

    async def update(self, item_id: int, content: str, rank: int):
        await self._db.execute(
            update(ItemModel)
            .filter(ItemModel.id == item_id)
            .values(content=content, rank=rank)
        )
        await self._db.commit()

    async def update_ranks_for_topic(self, topic_id: int, rank: int):
        await self._db.execute(
            update(ItemModel)
            .where(
                and_(
                    ItemModel.topic_id == topic_id,
                    ItemModel.rank >= rank
                )
            )
            .values(rank=ItemModel.rank + 1)
        )
        await self._db.commit()

    async def get_max_rank(self, topic_id: int) -> int:
        return (await self._db.scalars(
            select(func.max(ItemModel.rank))
            .where(ItemModel.topic_id == topic_id)
            .limit(1)
        )).one() or 0
