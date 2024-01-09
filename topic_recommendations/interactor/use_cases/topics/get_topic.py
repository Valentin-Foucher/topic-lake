from topic_recommendations.interactor.exceptions import DoesNotExist
from topic_recommendations.interactor.interfaces.base import Presenter
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class GetTopic(UseCase):
    def __init__(self, presenter: Presenter, repository: ITopicsRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self, topic_id: int):
        result = self._repository.get(topic_id)
        if not result:
            raise DoesNotExist(f'Topic {topic_id} does not exist')

        return self._presenter.present(result)
