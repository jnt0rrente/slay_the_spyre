from model.map.map import MapGenerator
from pprint import pprint

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as namedColors
import matplotlib.lines as mlines

import yaml 
import random

class MapTest:
    @staticmethod
    def get_args_for_map_generator(config_path="../config/game.yml"):
        with open(config_path) as f:
            game_config = yaml.load(f, Loader=yaml.FullLoader)
            acts_config = game_config["game"]["acts"]
            map_config = game_config["game"]["map"]
            
        return acts_config, map_config
    
    @staticmethod
    def set_random_seed(seed):
        random.seed(seed)
        np.random.seed(seed)
    
    @staticmethod
    def testSinglePathGeneration(config_path):
        acts_config, map_config = MapTest.get_args_for_map_generator(config_path)
        mapGen = MapGenerator(act_config=acts_config[0], map_config=map_config)
        
        print("Independent path from index 0:", mapGen._generate_path(0))
        print("Independent path from index 3:", mapGen._generate_path(3))
        print("Independent path from index 6:", mapGen._generate_path(6))
        
    @staticmethod
    def testMultiPathGeneration(config_path):
        acts_config, map_config = MapTest.get_args_for_map_generator(config_path)
        mapGen = MapGenerator(act_config=acts_config[0], map_config=map_config)
        paths = mapGen._generate_paths()
        pprint(paths)
        
        matrix = np.zeros((15, 10))
        plt.imshow(matrix, cmap='Greys', interpolation='nearest')
        plt.gca().invert_yaxis()
        plt.yticks(np.arange(0, matrix.shape[0], 1))
        plt.xticks(np.arange(0, matrix.shape[1], 1))
        
        #plot connected rooms as points
        colors = [namedColors.TABLEAU_COLORS[name] for name in ["tab:blue", "tab:red", "tab:orange", "tab:green", "tab:purple", "tab:pink"]]
        for path_number, path in enumerate(paths): #[1, 1, 0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 1, 1, 0, 0]
            for floor, room in enumerate(path):
                plt.scatter(room, floor, color=colors[path_number], zorder=2) #invert room/floor because x/y
            
        #plot lines connecting same color rooms
        for path_number, path in enumerate(paths): #[1, 1, 0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 1, 1, 0, 0]
            for floor in range(len(path)-1):
                x_coords = [path[floor], path[floor+1]]
                y_coords = [floor, floor+1]
                plt.plot(x_coords, y_coords, color=colors[path_number], zorder=2)
        
        legend_handles = [mlines.Line2D([], [], color=color, marker='o', markersize=10, label=f'Path {i}') for i, color in enumerate(colors)]
        plt.legend(handles=legend_handles, loc="upper right")

        plt.grid(True,zorder=1)
        plt.show()
        
    @staticmethod
    def testPathGenerationAndRoomPopulation(config_path):
        acts_config, map_config = MapTest.get_args_for_map_generator(config_path)
        MapTest.set_random_seed(42)
        mapGen = MapGenerator(act_config=acts_config[0], map_config=map_config, debug=True)
        room_map = mapGen.generate_act_map()
        room_map.display()