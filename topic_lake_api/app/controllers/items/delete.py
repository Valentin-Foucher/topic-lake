from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.domain.interfaces.repositories import IItemsRepository
from topic_lake_api.use_cases.items.delete import DeleteItem


class DeleteItemController(Controller):
    def __init__(self, repository: IItemsRepository):
        self._repository = repository

    def execute(self, user_id: int, item_id: int):
        DeleteItem(self._repository).execute(user_id, item_id)

