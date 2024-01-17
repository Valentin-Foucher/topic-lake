from topic_recommendations.app.controllers.base import Controller
from topic_recommendations.app.presenters.topics import GetTopicPresenter
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_recommendations.interactor.use_cases.topics.get_topic import GetTopic


class GetTopicController(Controller):
    def __init__(self, presenter: GetTopicPresenter, repository: ITopicsRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self, topic_id: int):
        result = GetTopic(self._repository).execute(topic_id)
        return self._presenter.present(result)

