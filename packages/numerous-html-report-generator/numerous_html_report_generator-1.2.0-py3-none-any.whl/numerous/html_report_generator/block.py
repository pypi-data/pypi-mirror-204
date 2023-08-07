from abc import ABC, abstractmethod
class Block(ABC):

    @abstractmethod
    def _as_html(self):
        ...
