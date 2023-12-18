from dataclasses import dataclass

from topic_recommendations.domain.entities.items import Item
from topic_recommendations.interactor.dtos.outputs.base import OutputDto


@dataclass
class ListItemsOutputDto(OutputDto):
    item_list: list[Item]


@dataclass
class GetItemOutputDto(OutputDto):
    item: Item
