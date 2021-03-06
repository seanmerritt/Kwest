import arcade
from game import CONSTANTS
import os
from game.SpriteWithHealth import SpriteWithHealth
from game.director import MyGame

def main():
    """ Main method """
    
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()