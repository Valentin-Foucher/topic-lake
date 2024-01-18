from typing import Optional

from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.interactor.interfaces.base import Presenter
from topic_lake_api.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_lake_api.interactor.interfaces.repositories.users import IUsersRepository
from topic_lake_api.interactor.use_cases.topics.create_topic import CreateTopic


class CreateTopicController(Controller):
    def __init__(self, presenter: Presenter, topics_repository: ITopicsRepository, users_repository: IUsersRepository):
        self._presenter = presenter
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    def execute(self, user_id: int, parent_topic_id: Optional[int], content: str):
        result = CreateTopic(self._topics_repository, self._users_repository).execute(
            user_id,
            parent_topic_id,
            content
        )
        return self._presenter.present(result)

