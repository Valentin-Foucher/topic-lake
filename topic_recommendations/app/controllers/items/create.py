from topic_recommendations.app.controllers.base import Controller
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository
from topic_recommendations.interactor.use_cases.items.create_item import CreateItem


class CreateItemController(Controller):
    def __init__(self, repository: IItemsRepository):
        self._repository = repository

    def execute(self, topic_id: int, user_id: int, content: str):
        CreateItem(self._repository).execute(topic_id, user_id, content)

