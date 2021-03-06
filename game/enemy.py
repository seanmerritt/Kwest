import arcade
from game.SpriteWithHealth import SpriteWithHealth
from game import CONSTANTS
import math

class enemy(arcade.Sprite):
    def __init(self,image,
                           scale,
                           image_x,
                           image_y,
                           image_width,
                           image_height,
                           flipped_horizontally,
                           flipped_vertically,
                           flipped_diagonally,
                           hit_box_algorithm,
                           hit_box_detail):
        super().__init__(image,
                           scale,
                           image_x,
                           image_y,
                           image_width,
                           image_height,
                           flipped_horizontally,
                           flipped_vertically,
                           flipped_diagonally,
                           hit_box_algorithm,
                           hit_box_detail)
        self.__shooting = False
        
    def shoot(self, player_x, player_y):
            start_x = self.center_x
            start_y = self.center_y

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
            if self.frame_count % 60 == 0:
                self.__shooting = True
                bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
                bullet.center_x = start_x
                bullet.center_y = start_y

                # Angle the bullet sprite
                bullet.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

                return bullet
    
    arcade.Sprite()