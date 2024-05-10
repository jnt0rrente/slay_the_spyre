import random

class EventChoice:
    def __init__(self, name, id, onPick):
        self.name = name
        self.id = id
        self.onPick = onPick
        
    @staticmethod
    def from_dict(choice_dict):
        return EventChoice(choice_dict['name'], choice_dict['id'], choice_dict['onPick'])
        
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
    def onPick(self):
        return self._onPick

    @onPick.setter
    def onPick(self, value):
        self._onPick = value

class Event:
    @staticmethod
    def from_dict(event_dict):
        return Event(event_dict["name"], 
                     event_dict["id"], 
                     event_dict["options"], 
                     [EventChoice.from_dict(choice) for choice in event_dict["choices"]])
        
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
    def options(self):
        return self._options
    
    @options.setter
    def options(self, value):
        self._options = value
    
    @property
    def possible_choices(self):
        return self._possible_choices
    
    @possible_choices.setter
    def possible_choices(self, value):
        self._possible_choices = value
    
    @property
    def choices(self):
        if not hasattr(self, "_choices"):
            self.build(self.options, self._choices)
        return self._choices
    
    @choices.setter
    def choices(self, value):
        self._choices = value
    
    def runRandom(self):
        if (self.options["choice_pick_algorithm"] == "random"):
            size_to_pick = self.options["choice_subset_size"]
            sample = random.sample(self.possible_choices, size_to_pick)
            
            self.choices = {elem.id: elem for elem in sample}
        return self
        
    