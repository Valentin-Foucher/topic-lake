from topic_recommendations.app.controllers.base import Controller
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository


class DeleteTopicController(Controller):
    _repository: ITopicsRepository

    def execute(self):
        pass
