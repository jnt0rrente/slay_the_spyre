from ..buyable import Buyable

class Relic(Buyable):
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
        
    #Implementing Buyable
    def add_to(self, player):
        player.relics.append(self)