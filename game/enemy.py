import arcade
from game.SpriteWithHealth import SpriteWithHealth
from game import CONSTANTS

class Enemy(SpriteWithHealth):
    def __init(self, image, scale, max_health):
        super().__init__()
        