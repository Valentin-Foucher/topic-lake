from topic_recommendations.app.controllers.base import Controller
from topic_recommendations.app.presenters.items import GetItemPresenter
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository
from topic_recommendations.interactor.use_cases.items.get_item import GetItem


class GetItemController(Controller):
    def __init__(self, presenter: GetItemPresenter, repository: IItemsRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self, item_id: int):
        return GetItem(self._presenter, self._repository).execute(item_id)

