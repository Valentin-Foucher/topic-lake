from abc import ABC, abstractmethod
from typing import Any


class ValueObject(ABC):
    def __init__(self, **kwargs):
        self._repr = kwargs

    @abstractmethod
    def get(self) -> Any:
        pass
