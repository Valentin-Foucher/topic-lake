from topic_recommendations.interactor.interfaces.base import Presenter
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class GetItem(UseCase):
    def __init__(self, presenter: Presenter, repository: IItemsRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self, item_id: int):
        result = self._repository.get(item_id)
        return self._presenter.present(result)
