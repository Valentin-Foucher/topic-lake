from topic_recommendations.app.presenters.topics import ListTopicsPresenter, GetTopicPresenter
from topic_recommendations.app.views.base import Controller
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_recommendations.interactor.use_cases.topics.create_topic import CreateTopic
from topic_recommendations.interactor.use_cases.topics.delete_topic import DeleteTopic
from topic_recommendations.interactor.use_cases.topics.get_topic import GetTopic
from topic_recommendations.interactor.use_cases.topics.list_topics import ListTopics


class TopicsUsers(Controller):
    _repository: ITopicsRepository

    def list(self):
        return ListTopics(ListTopicsPresenter(), self._repository).execute()

    def get(self, topic_id: int):
        return GetTopic(GetTopicPresenter(), self._repository).execute(topic_id)

    def create(self, user_id: int, content: str):
        CreateTopic(self._repository).execute(user_id, content)

    def delete(self, topic_id: int):
        DeleteTopic(self._repository).execute(topic_id)
