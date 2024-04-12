from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.app.presenters.items import GetItemPresenter
from topic_lake_api.domain.interfaces.repositories import IItemsRepository
from topic_lake_api.interactor.use_cases.items.get import GetItem


class GetItemController(Controller):
    def __init__(self, presenter: GetItemPresenter, repository: IItemsRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self, item_id: int):
        result = GetItem(self._repository).execute(item_id)
        return self._presenter.present(result)

