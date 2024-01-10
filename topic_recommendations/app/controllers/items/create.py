from topic_recommendations.app.controllers.base import Controller
from topic_recommendations.interactor.interfaces.base import Presenter
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_recommendations.interactor.interfaces.repositories.users import IUsersRepository
from topic_recommendations.interactor.use_cases.items.create_item import CreateItem


class CreateItemController(Controller):
    def __init__(self, presenter: Presenter, items_repository: IItemsRepository, topics_repository: ITopicsRepository,
                 users_repository: IUsersRepository):
        self._presenter = presenter
        self._items_repository = items_repository
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    def execute(self, topic_id: int, user_id: int, content: str):
        return CreateItem(
            self._presenter, self._items_repository, self._topics_repository, self._users_repository
        ).execute(topic_id, user_id, content)

