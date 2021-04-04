"""Enemy.py: file that contains the "enemy" class (only class in the file)
Over time, the enemies get smart after you start wiping a number of them out and try to use their invisibility powers. """
import arcade
from game.SpriteWithHealth import SpriteWithHealth
from game import CONSTANTS
import math

class enemies(arcade.SpriteList):
    """Contains code for the enemy sprites
    Methods in Class:
    - __init__(self, enemy_list, max_health)
    - shoot(self, player_x, player_y, frame_count, bullet_list)
    - draw_health_number(self)
    - draw_health_bar(self)
    """
    def __init__(self, enemy_list, max_health):
        """Constructor for the enemy class.
        """
        super().__init__()
        
        self.__shooting = False
        self.enemy_list = enemy_list
        self.max_health = max_health
        for enemy in self.enemy_list:
            setattr(enemy, 'max_health', self.max_health)
            setattr(enemy, 'cur_health', self.max_health)
            setattr(enemy, 'dead', False)
        self.sprite_list = self.enemy_list.sprite_list
        

    def shoot(self, player_x, player_y, frame_count, bullet_list):
        """Establishes Enemy shooting code"""
        for enemy in self.sprite_list:
            start_x = enemy.center_x
            start_y = enemy.center_y

            # Get the destination location for the bullet
            dest_x = player_x
            dest_y = player_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the self to face the player.
            self.angle = math.degrees(angle)-90

            # Shoot every 60 frames change of shooting each frame
            if frame_count % 60 == 0:
                self.__shooting = True
                bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
                bullet.center_x = start_x
                bullet.center_y = start_y

                # Angle the bullet sprite
                bullet.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                bullet.change_x = math.cos(angle) * CONSTANTS.BULLET_SPEED
                bullet.change_y = math.sin(angle) * CONSTANTS.BULLET_SPEED

                bullet_list.append(bullet)

    
    def draw_health_number(self):
        """ Draw how many hit points we have """
        for enemy in self.sprite_list:
            health_string = f"{enemy.cur_health}/{enemy.max_health}"
            arcade.draw_text(health_string,
                            start_x=enemy.center_x + CONSTANTS.HEALTH_NUMBER_OFFSET_X,
                            start_y=enemy.center_y + CONSTANTS.HEALTH_NUMBER_OFFSET_Y,
                            font_size=12,
                            color=arcade.color.WHITE)

    def draw_health_bar(self):
        """ Draw the health bar """
        for enemy in self.sprite_list:
            # Draw the 'unhealthy' background
            if enemy.cur_health < enemy.max_health:
                arcade.draw_rectangle_filled(center_x=enemy.center_x,
                                            center_y=enemy.center_y + CONSTANTS.HEALTHBAR_OFFSET_Y,
                                            width=CONSTANTS.HEALTHBAR_WIDTH,
                                            height=3,
                                            color=arcade.color.RED)

            # Calculate width based on health
            health_width = CONSTANTS.HEALTHBAR_WIDTH * (enemy.cur_health / enemy.max_health)

            arcade.draw_rectangle_filled(center_x=enemy.center_x - 0.5 * (CONSTANTS.HEALTHBAR_WIDTH - health_width),
                                        center_y=enemy.center_y + CONSTANTS.HEALTHBAR_OFFSET_Y,
                                        width=health_width,
                                        height=CONSTANTS.HEALTHBAR_HEIGHT,
                                        color=arcade.color.GREEN)   