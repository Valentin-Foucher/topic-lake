from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.app.presenters.items import GetItemPresenter
from topic_lake_api.interactor.interfaces.repositories.items import IItemsRepository
from topic_lake_api.interactor.use_cases.items.get_item import GetItem


class GetItemController(Controller):
    def __init__(self, presenter: GetItemPresenter, repository: IItemsRepository):
        self._presenter = presenter
        self._repository = repository

    async def execute(self, item_id: int):
        result = await GetItem(self._repository).execute(item_id)
        return self._presenter.present(result)

