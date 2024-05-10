from abc import ABC, abstractmethod

class Buyable(ABC):
    @abstractmethod
    def add_to(self, player):
        pass