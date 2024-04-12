from abc import ABC, abstractmethod
from typing import Any


class Repository(ABC):
    def list(self, *args, **kwargs) -> list[Any]:
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def get(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def delete(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def exists(self, *args, **kwargs) -> bool:
        raise NotImplementedError


class Presenter(ABC):
    @abstractmethod
    def present(self, *args, **kwargs) -> dict[str, Any]:
        pass
