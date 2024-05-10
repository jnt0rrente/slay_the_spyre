from model.item.buyable import Buyable

class Player:
    def __init__(self, name, card_color, max_health, base_energy, base_gold, starter_relic, starter_deck):
        self.name = name
        self.card_color = card_color
        self.health, self.max_health = max_health, max_health
        self.base_energy = base_energy
        self.gold = base_gold
        self.relics = [starter_relic]
        self.deck = starter_deck
        self.modifiers = []
        
    @staticmethod
    def from_dict(player_dict):
        return Player(player_dict['name'],
                      player_dict['card_color'],
                      player_dict['base_health'], 
                      player_dict['base_energy'], 
                      player_dict['base_gold'],
                      player_dict['starter_relic'],
                      player_dict['starter_deck'])
        
    def loadStarterDeck(self, cards):
        oldDeck = self.deck
        self.deck = []
        print(oldDeck)
        for card_value_pair in oldDeck:
            [id, amount] = card_value_pair.split(":")
            for i in range(int(amount)):
                self.deck.append(cards[id])
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
        
    @property
    def card_color(self):
        return self._card_color
    
    @card_color.setter
    def card_color(self, value):
        self._card_color = value
    
    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        self._health = value
        
    @property
    def max_health(self):
        return self._max_health
    
    @max_health.setter
    def max_health(self, value):
        self._max_health = value
        
    @property
    def gold(self):
        return self._gold
    
    @gold.setter
    def gold(self, value):
        self._gold = value
        
    @property
    def modifiers(self):
        return self._modifiers
    
    @modifiers.setter
    def modifiers(self, value):
        self._modifiers = value
        
    @property
    def relics(self):
        return self._relics
    
    @relics.setter
    def relics(self, value):
        self._relics = value
        
    @property
    def deck(self):
        return self._deck
    
    @deck.setter
    def deck(self, value):
        self._deck = value
        
    @property
    def energy(self):
        return self._energy
    
    @energy.setter
    def energy(self, value):
        self._energy = value
        
    @property
    def base_energy(self):
        return self._base_energy
    
    @base_energy.setter
    def base_energy(self, value):
        self._base_energy = value
        
    @property
    def potions(self):
        return self._potions
    
    @potions.setter
    def potions(self, value):
        self._potions = value
        
    def on_combat_end(self):
        self.modifiers = []
        
    def on_floor_end(self):
        self.full_heal()
        
    def full_heal(self):
        self.health = self.max_health
        
    def gain_max_hp(self, amount):
        self.max_health += amount
        self.health += amount
        
    def can_lose_max_hp(self, amount):
        return (self.max_health - amount) >= 1
        
    def lose_max_hp(self, amount):
        if not self.can_lose_max_hp(amount):
            raise ValueError("Cannot lose this amount of max hp.")
        else:
            self.max_health -= amount
        
    def gain_gold(self, amount):
        self.gold += amount
        
    def lose_gold(self, amount):
        if (amount > self.gold):
            raise ValueError("There is not enough gold to buy this item.")
        else:
            self.gold -= amount
        
    def can_buy(self, value):
        if (self.gold >= value):
            return True
        else:
            return False
        
    def buy(self, item: Buyable, value):
        try:
            self.spend_gold(value)
            item.add_to(self)
        except AttributeError:
            raise TypeError("This item is not a Buyable item.")