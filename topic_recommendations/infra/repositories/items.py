from sqlalchemy import select

from topic_recommendations.domain.entities.items import Item
from topic_recommendations.infra.db.core import session
from topic_recommendations.infra.db.models import Item as ItemModel
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository


class ItemsRepository(IItemsRepository):
    @staticmethod
    def _get_by_id(item_id: int):
        return session.scalars(
            select(ItemModel).filter_by(id=item_id).limit(1)
        ).one()

    def create(self, user_id: int, topic_id: int, content: str):
        session.add(ItemModel(user_id=user_id, topic_id=topic_id, content=content))
        session.commit()

    def get(self, item_id: int) -> Item:
        item = self._get_by_id(item_id)
        return Item(**item.mappings().all())

    def delete(self, item_id: int):
        item = self._get_by_id(item_id)
        session.delete(item)
        session.commit()

    def list(self, limit: int = 100) -> list[Item]:
        item_list = session.scalars(
            select(ItemModel).limit(limit)
        ).all()
        return [Item(**item.mappings().all()) for item in item_list]
