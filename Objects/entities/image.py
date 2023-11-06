from abc import ABC, abstractmethod

from pygame import Surface

class Image(ABC):
    @abstractmethod
    def get_surface(self) -> Surface:
        pass