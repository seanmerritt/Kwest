import arcade
from game import CONSTANTS
import os
from game.SpriteWithHealth import SpriteWithHealth
from game.director import *
from game.menus import *

def main():
    """ Main method """
    
    window = arcade.Window(CONSTANTS.SCREEN_WIDTH, CONSTANTS.SCREEN_HEIGHT, CONSTANTS.SCREEN_TITLE)
    start_view = MenuView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()


arcade.View() 