from topic_recommendations.app.presenters.topics import GetTopicPresenter
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class GetTopic(UseCase):
    def __init__(self, presenter: GetTopicPresenter, repository: ITopicsRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self, topic_id: int):
        result = self._repository.get(topic_id)
        return self._presenter.present(result)
