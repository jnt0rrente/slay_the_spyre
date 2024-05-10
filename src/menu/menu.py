from abc import ABC, abstractmethod
from model.game.game import GameState

class View(ABC):
    def __init__(self, game):
        self.game = game
        
    @abstractmethod
    def handle_input(self):
        pass

    def frame(self):
        print("\033[H\033[J")
        print("--------------------")
        if self.game.state != GameState.PLAYER_SELECTION:
            print(f"HP: {self.game.player.health}/{self.game.player.max_health} | Gold: {self.game.player.gold} | Potions: {'nyi'} | Deck: {len(self.game.player.deck)} | Relics: {len(self.game.player.relics)}")
            print("--------------------")
     
    @abstractmethod
    def render(self):
        pass
    
class EventView(View):
    def __init__(self, game):
        super().__init__(game)
    
    def render(self):
        self.frame()
        print("EventView")
        print("Event:", self.game.current_event.name)
        
    def handle_input(self):
        choiceList = list(self.game.current_event.choices.values())
        for i, choice in enumerate(choiceList):
            print(f"{i + 1}. {choice.name}")
        option = input("Select an option: ")
        
        if option.isdigit():
            choice = choiceList[int(option) - 1]
            print(f"You have chosen: {choice.name}")
            self.game.on_picked_choice(choice)
    
class MapView(View):
    def __init__(self, game):
        super().__init__(game)
        
    def render(self):
        self.frame()
        print("MapView")
        
    def handle_input(self):
        input("Press any key to continue...")
    
class CombatView(View):
    def __init__(self, game):
        super().__init__(game)
        
    def handle_input(self):
        pass
    
    def render(self):
        self.frame()
    
class PlayerSelectionView(View):
    def __init__(self, game):
        super().__init__(game)
        
    def render(self):
        self.frame()
        print("Player Selection")
        for i, player in enumerate(self.game.available_players):
            print(f"{i + 1}. {player.name}")
            
    def handle_input(self):
        option = input("Select a character: ")
        
        if option.isdigit():
            player = self.game.available_players[int(option) - 1]
            print(f"You have chosen to play as The {player.name}.")
            self.game.on_player_selected(player)
    
    
    
class GameMenu:
    def __init__(self, game):
        self.game = game
    
    def run(self):
        self.game.start()
        while True:
            view = self.getViewForGameState()
            view.render()
            view.handle_input()
       
    def getViewForGameState(self):
        switcher = {
            GameState.EVENT: EventView,
            GameState.MAP: MapView,
            GameState.COMBAT: CombatView,
            GameState.PLAYER_SELECTION: PlayerSelectionView
        }

        ViewClass = switcher.get(self.game.state)

        if ViewClass is None:
            raise Exception("Invalid game state")

        return ViewClass(self.game)
    
    def display(self):
        pass
    