from topic_recommendations.app.controllers.base import Controller
from topic_recommendations.app.presenters.items import ListItemsPresenter
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository
from topic_recommendations.interactor.use_cases.items.list_items import ListItems


class ListItemsController(Controller):
    def __init__(self, presenter: ListItemsPresenter, repository: IItemsRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self, topic_id: int):
        result = ListItems(self._repository).execute(topic_id)
        return self._presenter.present(result)

