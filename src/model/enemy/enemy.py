from abc import abstractmethod, ABC
from enum import Enum

class EnemyType(Enum):
    NORMAL = "Normal"
    ELITE = "Elite"
    BOSS = "Boss"

class Enemy(ABC):
    
    def __init__(self, name, id, max_health, enemy_type):
        self.name = name
        self.id = id
        self.max_health = max_health
        self.health = max_health
        self.enemy_type = enemy_type
        
        self.modifiers = []
        self.currentIntent = None
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value
        
    @property
    def max_health(self):
        return self._max_health
    
    @max_health.setter
    def max_health(self, value):
        self._max_health = value
        
    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        self._health = value
        
    @property
    def currentIntent(self):
        return self._currentIntent
    
    @currentIntent.setter
    def currentIntent(self, value):
        self._currentIntent = value
        
    @property
    def enemy_type(self):
        return self._type
    
    @enemy_type.setter
    def enemy_type(self, value):
        if not isinstance(value, EnemyType):
            raise ValueError("enemy_type must be an instance of EnemyType Enum")
        self._type = value
        
    @property
    def modifiers(self):
        return self._modifiers
    
    @modifiers.setter
    def modifiers(self, value):
        self._modifiers = value