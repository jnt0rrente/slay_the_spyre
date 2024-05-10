from ..buyable import Buyable
from enum import Enum
from abc import ABC, abstractmethod

class CardType(Enum):
    ATTACK = "Attack"
    SKILL = "Skill"
    POWER = "Power"
    STATUS = "Status"
    CURSE = "Curse"
    
class CardRarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    SPECIAL = "Special"
    BASIC = "Basic"
    
class CardKeyword(Enum):
    EXHAUST = "Exhaust"
    INNATE = "Innate"
    ETHEREAL = "Ethereal"
    RETAIN = "Retain"
    
class CardColor(Enum):
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"
    COLORLESS = "Colorless"
    ALL = "All"
    
class CardTarget(Enum):
    PLAYER = "Player"
    SINGLE = "Single"
    ALL = "All"
    
class Card(Buyable):
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value 
        
    @property
    def energy_cost(self):
        return self._energy_cost
    
    @energy_cost.setter
    def energy_cost(self, value):
        self._energy_cost = value
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
        
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        self._description = value
    
    @property
    def rarity(self):
        return self._rarity
    
    @rarity.setter
    def rarity(self, value):
        if not isinstance(value, CardRarity):
            print(value)
            raise ValueError("rarity must be an instance of CardRarity Enum")
        self._rarity = value
        
    @property
    def card_type(self):
        return self._card_type
    
    @card_type.setter
    def card_type(self, value):
        if not isinstance(value, CardType):
            raise ValueError("card_type must be an instance of CardType Enum")
        self._card_type = value
        
    @property
    def target(self):
        return self._target
    
    @target.setter
    def target(self, value):
        if not isinstance(value, CardTarget):
            raise ValueError("target must be an instance of CardTarget Enum")
        self._target = value
        
    @property
    def keywords(self):
        return self._keywords
    
    @keywords.setter
    def keywords(self, value):
        for keyword in value:
            if not isinstance(keyword, CardKeyword):
                raise ValueError("keywords must be a list of CardKeyword Enum")
        self._keywords = value
        
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        if not isinstance(value, CardColor):
            raise ValueError("color must be an instance of CardColor Enum")
        
    @property
    def attributes(self):
        return self._attributes
    
    @attributes.setter
    def attributes(self, value):
        self._attributes = value
        
    #Implementing Buyable
    def add_to(self, player):
        player.deck.append(self)
        
    @abstractmethod
    def onDraw(self, player):
        pass
    
    @abstractmethod
    def onPlay(self, player, target_or_targets):
        pass
    
    @abstractmethod
    def onDiscard(self, player):
        pass
    
    @abstractmethod
    def onExhaust(self, player):
        pass
    
    def get_attribute(self, key):
        return self.attributes.get(key)