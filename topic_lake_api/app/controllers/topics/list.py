from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.app.presenters.topics import ListTopicsPresenter
from topic_lake_api.domain.interfaces.repositories import ITopicsRepository
from topic_lake_api.use_cases.topics.list import ListTopics


class ListTopicsController(Controller):
    def __init__(self, presenter: ListTopicsPresenter, repository: ITopicsRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self):
        result = ListTopics(self._repository).execute()
        return self._presenter.present(result)

