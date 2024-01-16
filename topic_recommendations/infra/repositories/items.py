from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from topic_recommendations.domain.entities.items import Item
from topic_recommendations.infra.db.core import session
from topic_recommendations.infra.db.models import Item as ItemModel
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository


class ItemsRepository(IItemsRepository):
    def list(self, topic_id: int, limit: int = 100) -> list[Item]:
        item_list = session.scalars(
            select(ItemModel)
            .where(ItemModel.topic_id == topic_id)
            .limit(limit)
        ).all()
        return [item.as_dataclass() for item in item_list]

    def create(self, topic_id: int,  user_id: int, content: str):
        i = ItemModel(topic_id=topic_id,
                      user_id=user_id,
                      content=content)
        session.add(i)
        session.flush()
        session.commit()
        return i.id

    def get(self, item_id: int) -> Optional[Item]:
        try:
            item = session.scalars(
                select(ItemModel)
                .where(ItemModel.id == item_id)
                .limit(1)
            ).one()
        except NoResultFound:
            return None

        return item.as_dataclass()

    def delete(self, item_id: int) -> bool:
        deleted_rows = session.execute(
            ItemModel.__table__.delete()
            .where()
            .returning(ItemModel.id)
        ).fetchall()
        return len(deleted_rows) != 0
