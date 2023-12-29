from topic_recommendations.app.controllers.base import Controller
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository
from topic_recommendations.interactor.use_cases.items.create_item import CreateItem


class CreateItemController(Controller):
    def __init__(self, repository: IItemsRepository):
        self._repository = repository

    def execute(self, user_id: int, topic_id: int, content: str):
        CreateItem(self._repository).execute(user_id, topic_id, content)

