from topic_recommendations.app.presenters.items import ListItemsPresenter
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class ListItems(UseCase):
    def __init__(self, presenter: ListItemsPresenter, repository: IItemsRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self):
        result = self._repository.list()
        return self._presenter.present(result)
