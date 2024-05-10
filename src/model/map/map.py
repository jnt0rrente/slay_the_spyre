import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from enum import Enum

class RoomType(Enum):
    MONSTER = "monster"
    EVENT = "event"
    ELITE = "elite"
    CAMPFIRE = "campfire"
    MERCHANT = "merchant"
    BOSS = "boss"
    CHEST = "chest"
    BOSS_CHEST = "boss_chest"

class Map:
    def __init__(self):
        self.floors = [[]]
        self.map_height = 0
        
    def display(self):
        matrix = np.zeros((17, 10))
        plt.imshow(matrix, cmap='Greys', interpolation='nearest')
        plt.gca().invert_yaxis()
        # Get the number of floors
        num_floors = matrix.shape[0]

        # Create the labels
        labels = [f"Floor {i+1} (index {i})" for i in range(num_floors)]

        # Set the yticks
        plt.yticks(np.arange(0, num_floors, 1), labels)
        #plt.xticks(np.arange(0, matrix.shape[1], 1))
        
        #plot rooms in the graph, looping over floors and ignoring none values
        color_map = {
            RoomType.MONSTER: "chocolate",
            RoomType.EVENT: "turquoise",
            RoomType.ELITE: "red",
            RoomType.CAMPFIRE: "forestgreen",
            RoomType.MERCHANT: "gold",
            RoomType.BOSS: "darkred",
            RoomType.CHEST: "cornflowerblue",
            RoomType.BOSS_CHEST: "cornflowerblue"
        }
        
        for i, floor in enumerate(self.floors):
            for j, room in enumerate(floor):
                if room is None:
                    continue
                plt.scatter(j, i, color=color_map[room.room_type], zorder=2)
                
        #plot lines connecting rooms
        for room in self.get_rooms():
            for next_room in room.next():
                x_coords = [room.room_index, next_room.room_index]
                y_coords = [room.height, next_room.height]
                plt.plot(x_coords, y_coords, color="black", zorder=0)

        
        #legend the dots colors
        legend_elements = [mlines.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map[room_type], markersize=10, label=room_type.value) for room_type in RoomType]
        plt.legend(handles=legend_elements, loc='upper right')
        
        plt.grid(True,zorder=1)
        plt.show()
        
    def get_rooms_at_height(self, height):
        return [room for room in self.floors[height] if room is not None]
    
    def get_rooms(self):
        return [room for floor in self.floors for room in floor if room is not None]
    
    def get_room_count(self):
        return len(self.get_rooms())
    
    def check_room_constraints(self, room, _debugMessage=None):
        isOk = True
        
        if room.room_type == RoomType.BOSS:
            if not room.has_next():
                if _debugMessage:
                    _debugMessage(f"Boss room {room} has no next room", tags=["room", "constraints"], color="red")
                isOk = False
        elif room.room_type == RoomType.BOSS_CHEST:
            if not room.has_previous():
                if _debugMessage:
                    _debugMessage(f"Boss chest room {room} has no previous room", tags=["room", "constraints"], color="red")
                isOk = False
            if room.has_next():
                if _debugMessage:
                    _debugMessage(f"Boss chest room {room} has next room", tags=["room", "constraints"], color="red")
                isOk = False
    
        if room.height == 0:
            if room.has_previous():
                if _debugMessage:
                    _debugMessage(f"First room {room} has previous room", tags=["room", "constraints"], color="red")
                isOk = False
        
        #not consecutive constraints: elite, shop, campfire, chest
        if room.room_type in [RoomType.ELITE, RoomType.MERCHANT, RoomType.CAMPFIRE, RoomType.CHEST]:
            for next_room in room.next():
                if next_room.room_type == room.room_type:
                    if _debugMessage:
                        _debugMessage(f"Room {room} has consecutive room of same type: {next_room} ({room.room_type})", tags=["room", "constraints"], color="red")
                    isOk = False
            for prev_room in room.prev():
                if prev_room.room_type == room.room_type:
                    if _debugMessage:
                        _debugMessage(f"Room {room} has previous room of same type: {prev_room} ({room.room_type})", tags=["room", "constraints"], color="red")
                    isOk = False
        
        #different siblings rule
        for parent in room.prev():
            siblings = [sibling for sibling in parent.next() if sibling != room]
            for sibling in siblings:
                if sibling.room_type == room.room_type:
                    if _debugMessage:
                        _debugMessage(f"Room {room} has sibling of same type: {sibling} ({room.room_type})", tags=["room", "constraints"], color="red")
                    isOk = False
                
        #minimum floor 6 for elite and campfire, also != 14 for campfire
        if room.room_type == RoomType.ELITE:
            if room.height < 6-1: #-1 for index
                if _debugMessage:
                    _debugMessage(f"Elite room {room} is below floor 6", tags=["room", "constraints"], color="red")
                isOk = False
            
        if room.room_type == RoomType.CAMPFIRE:
            if room.height < 6-1 or room.height == 14-1:
                if _debugMessage:
                    _debugMessage(f"Campfire room {room} is below floor 6 or at floor 14", tags=["room", "constraints"], color="red")
                isOk = False
            
        return isOk
        
    def check_global_constraints(self, _debugMessage=None):
        for floor in self.floors:
            for room in floor:
                if room is None:
                    continue
                if not self.check_room_constraints(room, _debugMessage):
                    return False
        return True
    
    def create_room(self, room_height, room_index):
        if room_height > self.map_height:
            if room_height - self.map_height > 1:
                raise ValueError("Cannot create room at height greater than 1 above the current height")
            self.map_height = room_height
            self.floors.append([])
            
        room = Room(room_height, room_index)
        
        #pad floor with None if necessary
        while len(self.floors[room_height]) <= room_index:
            self.floors[room_height].append(None)
            
        self.floors[room_height][room_index] = room
        
        return room
    
    def exists_room(self, room_height, room_index):
        if room_height > self.map_height:
            return False
        if room_index >= len(self.floors[room_height]):
            return False
        return self.floors[room_height][room_index] is not None
        
    def link_rooms(self, prev_height, prev_index, height, room_index):
        if prev_height != height - 1:
            raise ValueError("Cannot link rooms that are not on consecutive heights")
        if prev_index >= len(self.floors[prev_height]):
            raise ValueError("Cannot link room that does not exist")
        if room_index >= len(self.floors[height]):
            raise ValueError("Cannot link room that does not exist")
        
        prev_room = self.floors[prev_height][prev_index]
        room = self.floors[height][room_index]
        
        room.link(prev_room)

class Room: #each room is a node in the graph
    def __init__(self, height, room_index):
        self.next_rooms = []
        self.previous_rooms = []
        self.height = height
        self.room_index = room_index
        self.room_type = None
        
    def __str__(self):
        return f"({self.height}, {self.room_index})"
    
    def link(self, other_room):
        if other_room == self:
            raise ValueError("Cannot link room to itself")
        if other_room is None:
            raise ValueError("Cannot link to None")
        if other_room.height == self.height:
            raise ValueError("Cannot link rooms that are on the same height")
        if abs(other_room.height - self.height) != 1:
            raise ValueError("Cannot link rooms that are not on consecutive heights")
        
        if other_room.height > self.height:
            self.next_rooms.append(other_room)
            other_room.previous_rooms.append(self)
        else:
            self.previous_rooms.append(other_room)
            other_room.next_rooms.append(self)
        
    def __eq__(self, other):
        return self.height == other.height and self.room_index == other.room_index
    
    def has_next(self):
        return len(self.next_rooms) > 0
    
    def has_previous(self):
        return len(self.previous_rooms) > 0
    
    def next(self):
        yield from self.next_rooms
        
    def prev(self):
        yield from self.previous_rooms
        
    def get_next(self):
        return self.next_rooms

    def get_previous(self):
        return self.previous_rooms

class MapGenerator:
    def __init__(self, act_config, map_config, debug=False):
        self.room_map = Map()
        self.act_config = act_config
        self.map_config = map_config
        self.debug = debug
    
    def _validate_transition(self, room_index, floor_index, offset, paths):
        if offset == None:
            return False
        
        if (room_index + offset) not in range(0,7):
            return False
        
        for path in paths:
            if (path[floor_index + 1] != room_index): continue #skip path if it does not go into the room in front of us
            
            other_floor_offset = path[floor_index + 1] - path[floor_index]
            if (other_floor_offset == 1 and offset == -1) or (other_floor_offset == -1 and offset == 1):
                return False
            
        return True
            
    
    def _next_room_index(self, room_index, floor_index, paths):    
        offset = None
        
        while not self._validate_transition(room_index, floor_index, offset, paths):
            offset = random.randint(-1, 1)
            
        return room_index + offset
        
        
    def _generate_path(self, starting_index, paths=[]):
        path = [starting_index] #sequence of indices from 0 to 5. change from one to the next is always -1, 0 or 1
        
        next_index = starting_index
        for floor_index in range(0, 14):
            next_index = self._next_room_index(next_index, floor_index, paths)
            path.append(next_index)
            
        return path
            
    def transpose_map(self,my_map):
        return list(map(list, zip(*my_map)))
    
    def _generate_paths(self):
        paths = []
        prev_first_room = None
        
        
        for path_num_counter in range(6): # 6 paths
            self._debugMessage(f"Generating path {path_num_counter}", tags=["info", "path"], color="green")
            first_room_for_path = random.randint(0, 6)
            
            if (path_num_counter == 1):
                while first_room_for_path == prev_first_room: # change it until they are different. if they are, do nothing.
                    first_room_for_path = random.randint(0, 6)
            
            newpath = self._generate_path(first_room_for_path, paths)
                
            paths.append(newpath)
            prev_first_room = first_room_for_path
            
        #TODO: remove convergence from first to second floor?
        return paths
    
    def _generate_room_graph(self, paths):
        for path in paths:
            prev_height, prev_index = None, None
            for room_height, room_index in enumerate(path):
                if not self.room_map.exists_room(room_height, room_index):   
                    self.room_map.create_room(room_height, room_index)
                    self._debugMessage(f"Created room at height {room_height} and index {room_index}", tags=["info", "room", "created"], color="green")
                if prev_height != None:
                    self.room_map.link_rooms(prev_height, prev_index, room_height, room_index)
                    self._debugMessage(f"Linked room at height {prev_height} and index {prev_index} to room at height {room_height} and index {room_index}", tags=["info", "room", "linked"], color="cyan")
                prev_height, prev_index = room_height, room_index
        
        self._debugMessage("Creating level end rooms...", tags=["info", "room", "created"], color="green")
        last_rooms = self.room_map.get_rooms_at_height(14)
        self._debugMessage("Creating boss room...", tags=["info", "room", "created"], color="cyan")
        boss_room = self.room_map.create_room(15, 2)
        self._debugMessage("Creating chest room...", tags=["info", "room", "created"], color="cyan")
        boss_chest_room = self.room_map.create_room(16, 2)
        
        #link
        self._debugMessage("Linking last rooms to boss room...", tags=["info", "room", "linked"], color="cyan")
        for room in last_rooms:
            room.link(boss_room)
        
        self._debugMessage("Linking boss room to boss chest room...", tags=["info", "room", "linked"], color="cyan")
        boss_room.link(boss_chest_room)
    
    def _populateRooms(self):
        # STEP 1: Calculate the amount of rooms for each type, based on the weights and the number of rooms
        self._debugMessage("Determining room types...", tags=["info", "room", "type", "weights"], color="green")
        weights = self.map_config["weights"]
        typesBucket = []
        roomCount = self.room_map.get_room_count()
        self._debugMessage(f"Total room count: {roomCount}", tags=["info", "room", "type", "weights"], color="cyan")
        for room_type_raw, percentage in weights.items():
            room_type = RoomType[room_type_raw.upper()]
            amount = int(roomCount * percentage)
            self._debugMessage(f"Adding {amount} rooms of type {room_type}", tags=["info", "room", "type", "weights"], color="cyan")
            typesBucket.extend([room_type] * amount)
        
        #print counts
        counts = {room_type: typesBucket.count(room_type) for room_type in RoomType}
        self._debugMessage(f"Room types bucket determined: {counts} for a total of {len(counts)}/{roomCount} rooms", tags=["info", "room", "type", "weights"], color="cyan")
            
        # STEP 2: Fill the rooms with the types according to the preset floors
        self._debugMessage("Setting preset floors...", tags=["info", "room", "type", "preset"], color="green")
        for preset_floor in self.act_config["preset_floors"]:
            rooms = self.room_map.get_rooms_at_height(preset_floor["floor"])
            room_type = RoomType[preset_floor["type"].upper()]
            self._debugMessage(f"Setting {len(rooms)} rooms to type {room_type} at floor {preset_floor['floor']}", tags=["info", "room", "type", "preset"], color="cyan")
            for room in rooms:
                room.room_type = room_type
        
        # STEP 3: Fill the bucket with monster rooms until its length matches the total of untyped rooms
        self._debugMessage("Filling bucket with monster rooms...", tags=["info", "room", "type", "monster"], color="green")
        all_rooms = self.room_map.get_rooms()
        untyped_room_count = 0
        for room in all_rooms:
            if room.room_type is None:
                untyped_room_count += 1
        countBefore = len(typesBucket)
        while len(typesBucket) < untyped_room_count:
            typesBucket.append(RoomType.MONSTER)
        countAfter = len(typesBucket)
        self._debugMessage(f"Added {countAfter - countBefore} monster rooms to the bucket", tags=["info", "room", "type", "monster"], color="cyan")
        
        
        # STEP 4: Assign a random type to each untyped room, checking for constraints
        self._debugMessage("Assigning random types to untyped rooms...", tags=["info", "room", "type", "random"], color="green")
        for room in all_rooms:
            self._debugMessage("Shuffling bucket...", tags=["info", "room", "type", "random"], color="cyan")
            random.shuffle(typesBucket)
            if room.room_type is None:
                for room_type in typesBucket:
                    self._debugMessage(f"Trying to assign room {str(room)} to type {room_type}", tags=["info", "room", "type", "random"], color="blue")
                    room.room_type = room_type
                    self._debugMessage(f"Checking constraints for room {str(room)}", tags=["info", "room", "type", "random"], color="cyan")
                    if self.room_map.check_room_constraints(room, self._debugMessage):
                        self._debugMessage(f"Constraints met", tags=["info", "room", "type", "random"], color="cyan")
                        typesBucket.remove(room_type)
                        self._debugMessage(f"Removed {room_type} from bucket", tags=["info", "room", "type", "random"], color="cyan")
                        self._debugMessage(f"Room {str(room)} assigned to type {room_type}", tags=["info", "room", "type", "random"], color="green")
                        break
                    self._debugMessage(f"Constraints not met", tags=["info", "room", "type", "random"], color="red")
                    room.room_type = None
                    
        # STEP 5: check if there are any untyped rooms
        self._debugMessage("Checking for untyped rooms...", tags=["info", "room", "type", "random"], color="green")
        all_rooms = self.room_map.get_rooms()
        for room in all_rooms:
            if room.room_type is None:
                self._debugMessage(f"Room {str(room)} is untyped", tags=["info", "room", "type", "random"], color="cyan")
                room.room_type = RoomType.MONSTER
                self._debugMessage(f"Room {str(room)} assigned to type {RoomType.MONSTER}", tags=["info", "room", "type", "random"], color="cyan")
                
        # STEP 6: check global constraints
        self._debugMessage("Checking global constraints...", tags=["info", "room", "type", "random"], color="green")
        if not self.room_map.check_global_constraints(_debugMessage=self._debugMessage):
            self._debugMessage("Global constraints not met", tags=["info", "room", "type", "random"], color="red")
                
    
    def generate_act_map(self):
        self._debugMessage("Generating act map...", tags=["info", "lifecycle"], color="yellow")
        
        self._debugMessage("Generating paths...", tags=["info", "lifecycle"], color="yellow")
        paths = self._generate_paths()
        self._debugMessage("Paths generated", tags=["info", "lifecycle"], color="yellow")
        
        self._debugMessage("Generating room graph...", tags=["info", "lifecycle"], color="yellow")
        self._generate_room_graph(paths)
        self._debugMessage("Room graph generated", tags=["info", "lifecycle"], color="yellow")
        
        self._debugMessage("Populating rooms...", tags=["info", "lifecycle"], color="yellow")
        self._populateRooms()
        self._debugMessage("Rooms populated", tags=["info", "lifecycle"], color="yellow")
        
        self._debugMessage("Act map generated", tags=["info", "lifecycle"], color="magenta")
        return self.room_map
    
    def _debugMessage(self, message, tags=[], color=""):
        color_map = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "cyan": "\033[96m",
            "magenta": "\033[95m"
        }

        if self.debug:
            tags_str = "[" + " ".join(tags) + "]"
            color_code = color_map.get(color, "")
            reset_code = "\033[0m" if color else ""
            print(f"{color_code}[D] {tags_str} {message}{reset_code}")