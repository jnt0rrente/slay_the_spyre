import sys

from menu.menu import GameMenu
from model.game.game import GameBuilder

from test.test import MapTest

def test():
    print("Test Menu")
    print("1. Map generation")
    print("2. Exit")
    
    opt = int(input("Option: "))
    if opt == 1:
        print("\nMap generation")
        print("1. Single path generation")
        print("2. Multi path generation")
        print("3. Path generation and room population")
        
        opt = int(input("Option: "))
        if opt == 1:
            MapTest.testSinglePathGeneration(sys.argv[2])
        elif opt == 2:
            MapTest.testMultiPathGeneration(sys.argv[2])
        elif opt == 3:
            MapTest.testPathGenerationAndRoomPopulation(sys.argv[2])
    elif opt == 2:
        sys.exit()
 
def main():
    # test()
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            test()
    else:
        game_builder = GameBuilder()
        
        game = game_builder \
                    .load_cards() \
                    .load_enemies() \
                    .load_relics() \
                    .load_events() \
                    .load_players('../config/players.yml') \
                    .load_game_config('../config/game.yml') \
                    .build()
        menu = GameMenu(game)
        menu.run()
    
if __name__ == "__main__":
    main()