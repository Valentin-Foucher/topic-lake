from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.app.presenters.topics import ListTopicsPresenter
from topic_lake_api.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_lake_api.interactor.use_cases.topics.list_topics import ListTopics


class ListTopicsController(Controller):
    def __init__(self, presenter: ListTopicsPresenter, repository: ITopicsRepository):
        self._presenter = presenter
        self._repository = repository

    async def execute(self):
        result = await ListTopics(self._repository).execute()
        return self._presenter.present(result)

