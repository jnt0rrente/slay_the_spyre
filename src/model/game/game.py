import yaml
from enum import Enum
from model.player.player import Player
from model.item.card.cardCollection import loadAllCards
from model.event.eventCollection import loadAllEvents
from model.enemy.enemyCollection import loadAllEnemies
from model.event.event import EventChoice

class GameState(Enum):
    PLAYER_SELECTION = "PLAYER_SELECTION"
    MAP = "MAP"
    EVENT = "EVENT"
    COMBAT = "COMBAT"

class GameBuilder:
    @staticmethod
    def parse_config_file(path, key=None):
        with open(path) as f:
            return yaml.load(f, Loader=yaml.FullLoader)[key] if key else yaml.load(f, Loader=yaml.FullLoader)
    
    def load_cards(self):
        self.cards = loadAllCards()
        return self
    
    def load_enemies(self):
        self.enemies = loadAllEnemies()
        return self
    
    def load_relics(self):
        self.relics = []
        return self
    
    def load_events(self):
        self.events = loadAllEvents()
        return self
    
    def load_players(self, path):
        players_as_dict_list = self.parse_config_file(path, "players")
        
        retList = []
        for player in players_as_dict_list:
            retList.append(Player.from_dict(player))
            
        self.players = retList
        
        return self
    
    def load_game_config(self, path):
        self.gameConfig = self.parse_config_file(path, "game")
        return self
    
    def build(self):
        for player in self.players:
            player.loadStarterDeck(self.cards)
            
        return Game(self.players,
                    self.relics,
                    self.cards,
                    self.enemies,
                    self.events,
                    self.gameConfig)

class Game:
    @property
    def player(self):
        return self._player
    
    @player.setter
    def player(self, value):
        self._player = value
        
    @property
    def available_players(self):
        return self._available_players
        
    @available_players.setter
    def available_players(self, value):
        self._available_players = value
        
    @property
    def relics(self):
        return self._relics
    
    @relics.setter
    def relics(self, value):
        self._relics = value
        
    @property
    def cards(self):
        return self._cards
    
    @cards.setter
    def cards(self, value):
        self._cards = value
        
    @property
    def enemies(self):
        return self._enemies
    
    @enemies.setter
    def enemies(self, value):
        self._enemies = value
        
    @property
    def events(self):
        return self._events
    
    @events.setter
    def events(self, value):
        self._events = value
        
    @property
    def game_config(self):
        return self._game_config
    
    @game_config.setter
    def game_config(self, value):
        self._game_config = value
        
    @property
    def current_floor(self):
        return self._current_floor
    
    @current_floor.setter
    def current_floor(self, value):
        self._current_floor = value
        
    @property
    def starting_event(self):
        return self._starting_event
    
    @starting_event.setter
    def starting_event(self, value):
        self._starting_event = value
        
    @property
    def current_event(self):
        return self._current_event
    
    @current_event.setter
    def current_event(self, value):
        self._current_event = value    
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        if value not in GameState:
            raise ValueError(f"Invalid game state: {value}")
        self._state = value
    
    @property
    def act_maps(self):
        return self._act_maps
    
    @act_maps.setter
    def act_maps(self, value):
        self._act_maps = value
    
    def __init__(self, available_players, relics, cards, enemies, events, game_config):
        self._available_players = available_players
        self._relics = relics
        self._cards = cards
        self._enemies = enemies
        self._events = events
        self._game_config = game_config
        self._current_floor = 0
        
        starting_event_id = self.game_config.get("starting_event")
        if starting_event_id is None:
            raise ValueError("No starting event found in game config")
        self._starting_event = self.events[starting_event_id]
        
        
    def start(self):
        self.state = GameState.PLAYER_SELECTION
        
    def on_picked_choice(self, choice: EventChoice):
        choice.onPick(self)
        self.state = GameState.MAP
    
    def on_player_selected(self, player):
        self.player = player
        self.state = GameState.EVENT
        self.current_event = self.starting_event.runRandom()
        
    def advance_floor(self):
        self.player.on_floor_end()
        self.current_floor += 1
        
    def addRelic(self, relic_id):
        pass
        #self.player.relics.append(self.relics[relic_id])