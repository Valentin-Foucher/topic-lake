from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.interactor.interfaces.repositories.items import IItemsRepository
from topic_lake_api.interactor.use_cases.items.update_item import UpdateItem


class UpdateItemController(Controller):
    def __init__(self, items_repository: IItemsRepository):
        self._items_repository = items_repository

    async def execute(self, user_id: int, item_id: int, content: str, rank: int):
        await UpdateItem(self._items_repository).execute(
            item_id,
            content,
            rank
        )

