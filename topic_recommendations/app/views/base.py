from abc import ABC

from topic_recommendations.interactor.interfaces.repositories.base import Repository


class View(ABC):
    def __init__(self, repository: Repository):
        self._repository = repository
