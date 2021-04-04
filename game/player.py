"""Player.py: this file contains the 'player' class. (only class in file)
It would've been cool if the player could select which character they wanted play as, 
but we didn't think of that idea in time. So the player sprite is randomly dealt."""
from game.SpriteWithHealth import SpriteWithHealth
import arcade
from game import CONSTANTS
import random

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class Player(arcade.Sprite):
    """ Player Sprite
    Methods in Class:
    - __init__(self, max_health)
    - update_animation(self, delta_time: float = 1/60)
    - draw_health_number(self)
    - draw_health_bar(self)
    - check_life(self)
    - get_death(self)
    """
    def __init__(self, max_health):
        """Constructor, establishes intial code for the player Sprite"""
        super().__init__()

        # Add extra attributes for health
        self.max_health = max_health
        self.cur_health = max_health
        self.__death = False

        # Default to face-right
        self.character_face_direction = CONSTANTS.RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = CONSTANTS.CHARACTER_SCALING

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        characters_List = []
        characters_List.append(":resources:images/animated_characters/female_adventurer/femaleAdventurer")
        characters_List.append(":resources:images/animated_characters/female_person/femalePerson")
        characters_List.append(":resources:images/animated_characters/male_person/malePerson")
        characters_List.append(":resources:images/animated_characters/male_adventurer/maleAdventurer")
        characters_List.append(":resources:images/animated_characters/zombie/zombie")
        characters_List.append(":resources:images/animated_characters/robot/robot")

        main_path = characters_List[random.randrange(0,5)]

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)
        
        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time: float = 1/60):
        """Determins the animation of the player Sprite based on certain conditions"""

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == CONSTANTS.RIGHT_FACING:
            self.character_face_direction = CONSTANTS.LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == CONSTANTS.LEFT_FACING:
            self.character_face_direction = CONSTANTS.RIGHT_FACING

        # Climbing animation
        
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return
        

        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

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
                                     center_y=self.center_y + CONSTANTS.HEALTHBAR_OFFSET_Y,
                                     width=health_width,
                                     height=CONSTANTS.HEALTHBAR_HEIGHT,
                                     color=arcade.color.GREEN)

    def check_life(self):
        """determinds if the player Sprite is still alive"""
        if self.cur_health < 1:
            self.__death = True

    def get_death(self):
        """The player sprite is dead"""
        return self.__death