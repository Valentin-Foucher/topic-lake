from abc import ABC

from topic_recommendations.interactor.interfaces.repositories.base import Repository


class Controller(ABC):
    def __init__(self, repository: Repository):
        self._repository = repository