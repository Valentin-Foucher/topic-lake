from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class CreateItem(UseCase):
    def __init__(self, repository: IItemsRepository):
        self._repository = repository

    def execute(self, user_id: int, topic_id: int, content: str):
        self._repository.create(user_id, topic_id, content)
