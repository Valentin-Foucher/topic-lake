from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from topic_recommendations.domain.entities.items import Item
from topic_recommendations.infra.db.core import session
from topic_recommendations.infra.db.models import Item as ItemModel
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository


class ItemsRepository(IItemsRepository):
    @staticmethod
    def _get_by_id(item_id: int):
        try:
            return session.scalars(
                select(ItemModel)
                .where(ItemModel.id == item_id)
                .limit(1)
            ).one()
        except NoResultFound:
            return None

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

    def get(self, item_id: int) -> Item:
        item = self._get_by_id(item_id)
        return item.as_dataclass() if item else None

    def delete(self, item_id: int) -> bool:
        item = self._get_by_id(item_id)
        if not item:
            return False

        session.delete(item)
        session.commit()
        return True
