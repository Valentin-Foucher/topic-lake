from abc import ABC, abstractmethod
from typing import Any


class Repository(ABC):
    pass


class Presenter(ABC):
    @abstractmethod
    def present(self, *args, **kwargs) -> dict[str, Any]:
        pass
