from topic_recommendations.interactor.interfaces.base import Presenter
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class ListItems(UseCase):
    def __init__(self, presenter: Presenter, repository: IItemsRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self, topic_id: int):
        result = self._repository.list(topic_id)
        return self._presenter.present(result)
