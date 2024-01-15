import dataclasses

from topic_recommendations.domain.entities.items import Item
from topic_recommendations.interactor.interfaces.base import Presenter


class ListItemsPresenter(Presenter):
    def present(self, items_list: list[Item]):
        return {'items': [dataclasses.asdict(item) for item in items_list]}


class GetItemPresenter(Presenter):
    def present(self, item: Item):
        return {'item': dataclasses.asdict(item)}


class CreateItemPresenter(Presenter):
    def present(self, inserted_id: int):
        return {'id': inserted_id}
