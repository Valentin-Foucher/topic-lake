from topic_recommendations.app.controllers.base import Controller
from topic_recommendations.app.presenters.topics import ListTopicsPresenter
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_recommendations.interactor.use_cases.topics.list_topics import ListTopics


class ListTopicsController(Controller):
    def __init__(self, presenter: ListTopicsPresenter, repository: ITopicsRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self):
        return ListTopics(self._presenter, self._repository).execute()

