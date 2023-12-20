from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class DeleteItem(UseCase):
    def __init__(self, repository: IItemsRepository):
        self._repository = repository

    def execute(self, item_id: int):
        self._repository.delete(item_id)
