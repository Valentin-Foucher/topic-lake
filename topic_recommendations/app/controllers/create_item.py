from topic_recommendations.app.controllers.base import Controller
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository


class CreateItemController(Controller):
    _repository: IItemsRepository

    def execute(self):
        pass
