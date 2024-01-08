from abc import ABC, abstractmethod
from typing import Any


class Controller(ABC):
    """
    The controller is a design pattern which aim is to take the input it is given and to convert it into
    the form required by the business.
    """
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass
