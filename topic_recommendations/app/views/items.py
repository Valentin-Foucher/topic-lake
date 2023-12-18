from topic_recommendations.app.presenters.items import ListItemsPresenter, GetItemPresenter
from topic_recommendations.app.views.base import View
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository
from topic_recommendations.interactor.use_cases.create_item import CreateItem
from topic_recommendations.interactor.use_cases.delete_item import DeleteItem
from topic_recommendations.interactor.use_cases.get_item import GetItem
from topic_recommendations.interactor.use_cases.list_items import ListItems


class ItemsView(View):
    _repository: IItemsRepository

    def list(self):
        return ListItems(ListItemsPresenter(), self._repository).execute()

    def get(self, item_id: int):
        return GetItem(GetItemPresenter(), self._repository).execute(item_id)

    def create(self, user_id: int, topic_id: int, content: str):
        CreateItem(self._repository).execute(user_id, topic_id, content)

    def delete(self, item_id: int):
        DeleteItem(self._repository).execute(item_id)
