from abc import ABC, abstractmethod
from typing import Any

from topic_recommendations.interactor.dtos.outputs.base import OutputDto


class Presenter(ABC):
    @abstractmethod
    def present(self, output_dto: OutputDto) -> dict[str, Any]:
        pass
