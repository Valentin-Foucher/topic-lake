from topic_recommendations.app.controllers.base import Controller
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository
from topic_recommendations.interactor.use_cases.items.delete_item import DeleteItem


class DeleteItemController(Controller):
    def __init__(self, repository: IItemsRepository):
        self._repository = repository

    def execute(self, item_id: int):
        DeleteItem(self._repository).execute(item_id)

