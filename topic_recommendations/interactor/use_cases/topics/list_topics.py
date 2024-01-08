from topic_recommendations.interactor.interfaces.base import Presenter
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class ListTopics(UseCase):
    def __init__(self, presenter: Presenter, repository: ITopicsRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self):
        result = self._repository.list()
        return self._presenter.present(result)
