from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.domain.interfaces.repositories import IItemsRepository
from topic_lake_api.use_cases.items.update import UpdateItem


class UpdateItemController(Controller):
    def __init__(self, items_repository: IItemsRepository):
        self._items_repository = items_repository

    def execute(self, user_id: int, item_id: int, content: str, rank: int):
        UpdateItem(self._items_repository).execute(
            item_id,
            content,
            rank
        )
