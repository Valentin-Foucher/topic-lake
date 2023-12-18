from abc import ABC, abstractmethod

from topic_recommendations.interactor.interfaces.repositories.base import Repository


class Controller(ABC):
    def __init__(self, repository: Repository):
        self._repository = repository

    @abstractmethod
    def execute(self):
        pass
