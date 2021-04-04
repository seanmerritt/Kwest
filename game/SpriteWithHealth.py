"""SpriteWithHealt.py: this has the code for all sprites with health (enemies and players)"""
from game import CONSTANTS
import arcade

class SpriteWithHealth(arcade.Sprite):
    """ Sprite with hit points
    Methods in classes:
    - __init__(self, image, scale, max_health)
    - draw_health_number(self)
    - draw_health_bar(self)
     """

    def __init__(self, image, scale, max_health):
        """draws from other codes and establishes the health status of the sprites"""
        super().__init__(image, scale)

        # Add extra attributes for health
        self.max_health = max_health
        self.cur_health = max_health

    def draw_health_number(self):
        """ Draw how many hit points we have """

        health_string = f"{self.cur_health}/{self.max_health}"
        arcade.draw_text(health_string,
                         start_x=self.center_x + CONSTANTS.HEALTH_NUMBER_OFFSET_X,
                         start_y=self.center_y + CONSTANTS.HEALTH_NUMBER_OFFSET_Y,
                         font_size=12,
                         color=arcade.color.WHITE)

    def draw_health_bar(self):
        """ Draw the health bar """

        # Draw the 'unhealthy' background
        if self.cur_health < self.max_health:
            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y + CONSTANTS.HEALTHBAR_OFFSET_Y,
                                         width=CONSTANTS.HEALTHBAR_WIDTH,
                                         height=3,
                                         color=arcade.color.RED)

        # Calculate width based on health
        health_width = CONSTANTS.HEALTHBAR_WIDTH * (self.cur_health / self.max_health)

        arcade.draw_rectangle_filled(center_x=self.center_x - 0.5 * (CONSTANTS.HEALTHBAR_WIDTH - health_width),
                                     center_y=self.center_y - 10,
                                     width=health_width,
                                     height=CONSTANTS.HEALTHBAR_HEIGHT,
                                     color=arcade.color.GREEN)