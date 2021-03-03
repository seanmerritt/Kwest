import arcade
from game import CONSTANTS
import os
from game.SpriteWithHealth import SpriteWithHealth
from game.player import Player
import random

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(CONSTANTS.SCREEN_WIDTH, CONSTANTS.SCREEN_HEIGHT, CONSTANTS.SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # Set the path to start with this program
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        # Lists for the game
        self.coin_list = None
        self.player_list = None
        self.enemy_list = None
        self.box_list = None
        self.wall_list = None
        self.key_list = None
        self.enemy_list = None
        self.game_over = False
        #self.moving_platforms_list = None
        
        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our 'physics' engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        self.end_of_map = 0

        # Keep track of the score
        self.score = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
       # self.moving_platforms_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = Player(max_health= 10)

        self.player_sprite.center_x = CONSTANTS.PLAYER_START_X
        self.player_sprite.center_y = CONSTANTS.PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        # --- Load in a map from the tiled editor ---

        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        #moving_platforms_layer_name = 'Moving Platforms'

        # Name of the layer that has items for pick-up
        coins_layer_name = 'Coins'

        # Map name
        #map_name = f"C:/Users/seanm/OneDrive/Documents/BYU/Kwest/game/testing map.tmx"
        map_name = f":resources:tmx_maps/map_with_ladders.tmx"
        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = my_map.map_size.width * CONSTANTS.GRID_PIXEL_SIZE

        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(my_map,
                                                      platforms_layer_name,
                                                      CONSTANTS.TILE_SCALING,
                                                      use_spatial_hash=True)

        # -- Moving Platforms
       # moving_platforms_list = arcade.tilemap.process_layer(my_map, moving_platforms_layer_name, CONSTANTS.TILE_SCALING)
       # for sprite in moving_platforms_list:
        #    self.wall_list.append(sprite)

        # -- Background objects
        self.background_list = arcade.tilemap.process_layer(my_map, "Background", CONSTANTS.TILE_SCALING)

        # -- Background objects
        self.ladder_list = arcade.tilemap.process_layer(my_map, "Ladders", CONSTANTS.TILE_SCALING, use_spatial_hash=True)

        # -- Coins
        self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name,
                                                      CONSTANTS.TILE_SCALING,
                                                      use_spatial_hash=True)
        for i in range(CONSTANTS.NUMBER_OF_ENEMIES):

            # Create the coin instance
            # Coin image from kenney.nl
            enemy = SpriteWithHealth(":resources:images/enemies/wormGreen.png", CONSTANTS.SPRITE_SCALING, max_health=5)

            # --- IMPORTANT PART ---

            # Boolean variable if we successfully placed the coin
            enemy_placed_successfully = False

            # Keep trying until success
            while not enemy_placed_successfully:
                # Position the coin
                enemy.center_x = random.randrange(CONSTANTS.SCREEN_WIDTH)
                enemy.center_y = random.randrange(CONSTANTS.SCREEN_HEIGHT)

                # See if the coin is hitting a wall
                wall_hit_list = arcade.check_for_collision_with_list(enemy, self.wall_list)

                # See if the coin is hitting another coin
                enemy_hit_list = arcade.check_for_collision_with_list(enemy, self.enemy_list)

                if len(wall_hit_list) == 0 and len(enemy_hit_list) == 0:
                    # It is!
                    enemy_placed_successfully = True

            # Add the coin to the lists
            self.enemy_list.append(enemy)
        # --- Other stuff
        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant= CONSTANTS.GRAVITY,
                                                             ladders=self.ladder_list)


    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        # Draw our sprites
        self.wall_list.draw()
        self.background_list.draw()
        self.ladder_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        self.player_sprite.draw_health_bar()
        self.player_sprite.draw_health_number()
        self.enemy_list.draw()
        
        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)

        # Draw hit boxes.
        # for wall in self.wall_list:
        #     wall.draw_hit_box(arcade.color.BLACK, 3)
        #
        # self.player_sprite.draw_hit_box(arcade.color.RED, 3)
    
    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = CONSTANTS.PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump(y_distance=10) and not self.jump_needs_reset:
                self.player_sprite.change_y = CONSTANTS.PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -CONSTANTS.PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0
        
        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = CONSTANTS.PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -CONSTANTS.PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player with the physics engine
        self.physics_engine.update()

        # Update animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True
        
        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()
        
        self.coin_list.update_animation(delta_time)
        self.background_list.update_animation(delta_time)
        self.player_list.update_animation(delta_time)

        # Update walls, used with moving platforms
        self.wall_list.update()

        # See if the moving wall hit a boundary and needs to reverse direction.
        for wall in self.wall_list:

            if wall.boundary_right and wall.right > wall.boundary_right and wall.change_x > 0:
                wall.change_x *= -1
            if wall.boundary_left and wall.left < wall.boundary_left and wall.change_x < 0:
                wall.change_x *= -1
            if wall.boundary_top and wall.top > wall.boundary_top and wall.change_y > 0:
                wall.change_y *= -1
            if wall.boundary_bottom and wall.bottom < wall.boundary_bottom and wall.change_y < 0:
                wall.change_y *= -1

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.coin_list)

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:

            # Figure out how many points this coin is worth
            if 'Points' not in coin.properties:
                print("Warning, collected a coin without a Points property.")
            else:
                points = int(coin.properties['Points'])
                self.score += points

            # Remove the coin
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)

        # Track if we need to change the viewport
        changed_viewport = False

        # --- Manage Scrolling ---

        # Scroll left
        left_boundary = self.view_left + CONSTANTS.LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + CONSTANTS.SCREEN_WIDTH - CONSTANTS.RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        # Scroll up
        top_boundary = self.view_bottom + CONSTANTS.SCREEN_HEIGHT - CONSTANTS.TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed_viewport = True

        # Scroll down
        bottom_boundary = self.view_bottom + CONSTANTS.BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        if changed_viewport:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                CONSTANTS.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                CONSTANTS.SCREEN_HEIGHT + self.view_bottom)

        if not self.game_over:
            # Move the enemies
            self.enemy_list.update()

            # Check each enemy
            for enemy in self.enemy_list:
                # If the enemy hit a wall, reverse
                if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                    enemy.change_x *= -1
                # If the enemy hit the left boundary, reverse
                elif enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                    enemy.change_x *= -1
                # If the enemy hit the right boundary, reverse
                elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                    enemy.change_x *= -1

            # Update the player using the physics engine
            self.physics_engine.update()

            # See if the player hit a worm. If so, game over.
            if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 0:
                self.game_over = True
