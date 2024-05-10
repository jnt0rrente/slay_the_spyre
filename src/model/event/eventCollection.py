from model.event.event import Event, EventChoice

def loadAllEvents():
    return {
        event.id: event for event in [
            NeowEvent()
        ]
    }
    

class NeowEvent(Event):
    def __init__(self):
        super().__init__()
        self.id = "neow_start"
        self.name = "Neow"
        self.description = "Hello..."
        self.options = {
            "choice_pick_algorithm": "random",
            "choice_subset_size": 2
        }
        self.possible_choices = [
            EventChoice("Gain 7 max HP", "neow_1", onPick=lambda game: game.player.gain_max_hp(7)),
            EventChoice("Enemies in your next 3 battles have 1 HP", "neow_2", onPick=lambda game: game.add_relic("set1hp_3enemies"))
        ]