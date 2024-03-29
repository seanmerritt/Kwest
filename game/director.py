"""Directory: This is where most of the code that causes the game to work exists.
It calls for classes from other files and imports various libraries.

Classes in this file:
- GameView(arcade.View)
- GameOverView(arcade.View)
- PauseView(arcade.View)
- FinishView(arcade.View)
 """

import arcade
from game import CONSTANTS
import os
from game.SpriteWithHealth import SpriteWithHealth
from game.player import Player
import random
import math
from game.enemy import enemies
import time


class GameView(arcade.View):
    """
    Main application class. The game runs because of this class.

    Methods in this class:
    - Constructor (__init__(self))
    - setup(self)
    - on_draw(self)
    - on_key_press(self, key, modifiers)
    - on_key_release(self, key, modifiers)
    - on_update(self, delta_time)
    """

    def __init__(self):
        """establishes the variables and resources that the rest of the code will use"""

        # Call the parent class and set up the window
        super().__init__()

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
        self.game_start_time = time.time()
        self.game_end_time = 0

        # Lists for the game
        self.coin_list = None
        self.player_list = None
        self.enemy_list = None
        self.box_list = None
        self.wall_list = None
        self.key_list = None
        self.bullet_list = None
        self.booster_list = None
        self.finish_list = None
        
        self.my_bullet_list = None
        self.power_up_list = None
        self.dead_list = None
        self.can_shoot = False
        self.character_face_direction = "default"

        self.game_over = False
        #self.moving_platforms_list = None
        
        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our 'physics' engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0
        self.frame_count = 0
        self.end_of_map = 0

        # Keep track of the score
        self.score = 0
        self.kills = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.more_hp_sound = arcade.load_sound(":resources:sounds/upgrade4.wav")
        self.PowerUp_sound = arcade.load_sound(":resources:sounds/upgrade5.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        # self.game_over_sound = arcade.load_sound(":resources:sounds/gameover2.wav")
        self.enemy_dies_sound = arcade.load_sound(":resources:sounds/error5.wav")
        self.you_hurt_sound = arcade.load_sound(":resources:sounds/hurt3.wav")
        self.enemy_shoots_sound = arcade.load_sound(":resources:sounds/jump5.wav")


    def setup(self):
        """ Set up the game here. Call this function to restart the game. 
        Assigns each variable a starting value"""

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0
        self.kills = 0

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.finish_list = arcade.SpriteList()
        
        self.my_bullet_list = arcade.SpriteList()
        self.power_up_list = arcade.SpriteList()
        self.dead_list = arcade.SpriteList()
       #  self.moving_platforms_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = Player(max_health= 10)

        self.player_sprite.center_x = CONSTANTS.PLAYER_START_X
        self.player_sprite.center_y = CONSTANTS.PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        self.power_up = arcade.Sprite(":resources:images/items/gemRed.png", 0.5)
        self.power_up.center_x = CONSTANTS.PLAYER_START_X +500  #5250
        self.power_up.center_y = CONSTANTS.PLAYER_START_Y + 2000 #5800
        self.power_up_list.append(self.power_up)        

        # --- Load in a map from the tiled editor ---

        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        #moving_platforms_layer_name = 'Moving Platforms'

        # Name of the layer that has items for pick-up
        coins_layer_name = 'Coins'

        # Map name
        map_name = f"adventure_level.tmx"
        my_map = arcade.tilemap.read_tmx(map_name)

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = my_map.map_size.width * CONSTANTS.GRID_PIXEL_SIZE

        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(my_map,
                                                      platforms_layer_name,
                                                      CONSTANTS.TILE_SCALING)

        # -- Background objects
        self.background_list = arcade.tilemap.process_layer(my_map, "Background", CONSTANTS.TILE_SCALING)

        # -- Background objects
        self.ladder_list = arcade.tilemap.process_layer(my_map, "Ladders", CONSTANTS.TILE_SCALING, use_spatial_hash=True)

        # -- Coins
        self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name,
                                                      CONSTANTS.TILE_SCALING,
                                                     use_spatial_hash=True)
        self.enemy_list = enemies(arcade.tilemap.process_layer(my_map,"Enemies", CONSTANTS.TILE_SCALING), 3)

        self.finish_list = arcade.tilemap.process_layer(my_map,"Finish", CONSTANTS.TILE_SCALING)

        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)


        self.booster_list = arcade.tilemap.process_layer(my_map, "Boosters",
                                                      CONSTANTS.TILE_SCALING,
                                                     use_spatial_hash=True)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant= CONSTANTS.GRAVITY , 
                                                             ladders=self.ladder_list
                                                             )


    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()

        # Draw our sprites
        
        self.background_list.draw()
        self.wall_list.draw()
        self.ladder_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        self.player_sprite.draw_health_bar()
        self.player_sprite.draw_health_number()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.enemy_list.draw_health_bar()
        self.enemy_list.draw_health_number()
        self.booster_list.draw()
        self.finish_list.draw()
        
        self.my_bullet_list.draw()
        self.power_up_list.draw()
        self.dead_list.draw()
        
        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)
    
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
            self.character_face_direction = "up"
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
            self.character_face_direction = "down"
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
            self.character_face_direction = "left"
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
            self.character_face_direction = "right"
        elif key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)

        # the player can shoot after they get the power up item and if they press the SPACE bar
        if (key == arcade.key.SPACE) and (self.can_shoot):
            #create and place the bullet
            my_bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png")
            my_bullet.center_y = self.player_sprite.center_y - 20

            #set the direction the bullet will go
            if self.character_face_direction == "left":
                my_bullet.center_x = self.player_sprite.center_x - 20
                my_bullet.angle = 90
                my_bullet.change_x =  -CONSTANTS.MY_BULLET_SPEED  
            elif self.character_face_direction == "right":
                my_bullet.center_x = self.player_sprite.center_x + 20
                my_bullet.angle = -90
                my_bullet.change_x =  CONSTANTS.MY_BULLET_SPEED
            elif self.character_face_direction == "up":
                my_bullet.center_x = self.player_sprite.center_x
                my_bullet.angle = 0
                my_bullet.change_x = 0
                my_bullet.change_y = CONSTANTS.MY_BULLET_SPEED
            elif self.character_face_direction == "down":
                my_bullet.center_x = self.player_sprite.center_x
                my_bullet.angle = 180
                my_bullet.change_x = 0
                my_bullet.change_y = -CONSTANTS.MY_BULLET_SPEED

            #add bullet to list so it is drawn when called
            self.my_bullet_list.append(my_bullet)               

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
        """ Movement and game logic. 
        Determines the change that occurs in the game as time progresses and variables change """

        #if player health =0 kill them
        if self.player_sprite.cur_health ==0:     
            death = GameOverView(self)
            self.window.show_view(death)

        if self.player_sprite.center_y < -5:     
            death = GameOverView(self)
            self.window.show_view(death)

        # Move the player with the physics engine
        self.physics_engine.update()
        self.frame_count += 1
        
        self.enemy_list.shoot(self.player_sprite.center_x, self.player_sprite.center_y, self.frame_count, self.bullet_list)

        # Get rid of the bullet when it flies off-screen
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

            # Check this bullet to see if it hit a wall
            wallhit_list = arcade.check_for_collision_with_list(bullet, self.wall_list)

            # If it did, get rid of the bullet
            if len(wallhit_list) > 0:
                bullet.remove_from_sprite_lists()

            #Check this bullet to see if it hit at grave stone
            gravehit_list = arcade.check_for_collision_with_list(bullet, self.dead_list)
            if len(gravehit_list) > 0:
                bullet.remove_from_sprite_lists()


            playerhit_list = arcade.check_for_collision_with_list(bullet, self.player_list)

            # If it did, get rid of the bullet
            if len(playerhit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            if arcade.check_for_collision(bullet, self.player_sprite):
                
                self.player_sprite.cur_health -= 1
                arcade.play_sound(self.you_hurt_sound)
                

            # If the bullet flies off-screen, remove it.
            if bullet.top < 0 or bullet.right < 0:
                bullet.remove_from_sprite_lists()

        for my_bullet in self.my_bullet_list:
            if my_bullet.top < 0:
                my_bullet.remove_from_sprite_lists()

            # Check this bullet to see if it hit a wall
            wallhit_list2 = arcade.check_for_collision_with_list(my_bullet, self.wall_list)
            # If it did, get rid of the bullet
            if len(wallhit_list2) > 0:
                my_bullet.remove_from_sprite_lists()

            #Check this bullet to see if it hit an enemy
            enemyhit_list = arcade.check_for_collision_with_list(my_bullet, self.enemy_list)

            # If it did, get rid of the bullet
            for enemy in enemyhit_list:
                if (len(enemyhit_list) > 0) and (not enemy.dead):
                    my_bullet.remove_from_sprite_lists()
                    enemy.cur_health -= 1
                    if (enemy.cur_health <=0) and (not enemy.dead):
                        #creates tombstone sprite when enemy dies
                        dead = arcade.Sprite("png/Object/tombstone2.png", 0.3)
                        dead.center_x = enemy.center_x
                        dead.center_y = enemy.center_y+4.5
                        arcade.play_sound(self.enemy_dies_sound)
                        self.dead_list.append(dead)                            
                        #change state of enemy to dead so your bullets pass through 
                        setattr(enemy,'dead',True)
                        self.dead_list.append(enemy)
                        enemy.remove_from_sprite_lists()   
                        del enemy                         
                
            
            # If the bullet flies off-screen, remove it.
            if my_bullet.top < 0 or my_bullet.right < 0:
                my_bullet.remove_from_sprite_lists()

        self.bullet_list.update()
        self.my_bullet_list.update()
        self.enemy_list.update()
        
        #Allow Player to shoot once they touch the power gem
        if arcade.check_for_collision_with_list(self.player_sprite,self.power_up_list):
            self.can_shoot = True
            self.power_up.remove_from_sprite_lists()   
            arcade.play_sound(self.PowerUp_sound)     

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
        self.enemy_list.update_animation(delta_time)
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
            self.score += 1
            if self.score%50 ==0:
                self.player_sprite.cur_health += 3
                # self.player_sprite.cur_health = self.player_sprite.max_health
                arcade.play_sound(self.more_hp_sound)


            # Remove the coin
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)



        # See if we hit any health boost items
        boost_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.booster_list)

        # Loop through each health_boost we hit (if any) and remove it
        for boost in boost_hit_list:
            hp_diff = self.player_sprite.max_health - self.player_sprite.cur_health
            # how much health do you get
            if hp_diff  >= 3:
                self.player_sprite.cur_health += 3
            else:
                self.player_sprite.cur_health += hp_diff

            # Remove the healt boost item
            boost.remove_from_sprite_lists()
            arcade.play_sound(self.more_hp_sound)

        if arcade.check_for_collision_with_list(self.player_sprite,self.finish_list):
            ## Insert won game screen here!
            self.game_end_time = time.time()
            game_time = self.game_end_time - self.game_start_time
            win = FinishView(self, self.score, len(self.dead_list), game_time)
            self.window.show_view(win)
            

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

            # Update the player using the physics engine
            self.physics_engine.update()

            # See if the player hit a worm. If so, game over.
            if self.player_sprite.get_death:
                self.game_over = True
                self.player_sprite.remove_from_sprite_lists()

            

class GameOverView(arcade.View):
    """ View to show when game is over
    Methods in class:
    - wait_for_key(self, keh, _modifies)
    - __init__(self, game_view)
    - on_show(self)"
    - on_draw(self)
    - on_draw(self)"""

    #wait for key to be pressed to continue
    def wait_for_key(self, key, _modifiers):
        """Restarts the game after ENTER key is pressed"""
        if key == arcade.key.ENTER:  # reset game
            game = GameView()
            game.setup()
            self.window.show_view(game)

            
    #flavoring for text
    def __init__(self, game_view):
        """ This runs once when we switch to this view """
        super().__init__()
        self.game_view = game_view
        self.game_over_sound = arcade.load_sound(":resources:sounds/gameover2.wav")
        # self.texture = arcade.load_texture("game_over.jpg")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        

    def on_show(self):
        """shows black backdrop for endgame screen"""
        arcade.set_background_color(arcade.color.BLACK)
        arcade.play_sound(self.game_over_sound)

    def on_draw(self):
        """shows text for endgame screen"""
        arcade.start_render()

        WIDTH = (CONSTANTS.SCREEN_WIDTH + self.game_view.view_left) -  self.game_view.view_left
        HEIGHT = (CONSTANTS.SCREEN_HEIGHT + self.game_view.view_bottom) - self.game_view.view_bottom
        
        arcade.set_viewport(0, WIDTH - 1, 0, HEIGHT - 1)

        # self.texture.draw_sized(WIDTH / 2, HEIGHT / 2,
                                # WIDTH, HEIGHT)

        arcade.draw_text("GAME OVER", WIDTH/2, HEIGHT/2+50,
                         arcade.color.SCARLET, font_size=50, anchor_x="center")

        arcade.draw_text("Press the Space Bar to reset",
                         WIDTH/2,
                         HEIGHT/2-80,
                         arcade.color.SCARLET,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        """restarts game after SPACE bar is pressed"""
        if key == arcade.key.SPACE:  
            game = GameView()
            game.setup()
            self.window.show_view(game)




class PauseView(arcade.View):
    """
    Allows the Pause screen to pop up after ESC key is pressed
    Methods in Class:
    - __init__(self, game_view)
    - on_show(self)
    - on_draw(self)
    - on_key_press(self, key, _modifiers)
    """
    def __init__(self, game_view):
        """Constructor"""
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        """Sets the backdrop of the pause screen"""
        arcade.set_background_color(arcade.color.ORANGE)

    def on_draw(self):
        """draws the text for the pause screen"""
        arcade.start_render()

        # Draw player, for effect, on pause screen.
        # The previous View (GameView) was passed in
        # and saved in self.game_view.
        player_sprite = self.game_view.player_sprite
        player_sprite.draw()

        WIDTH = (CONSTANTS.SCREEN_WIDTH + self.game_view.view_left) -  self.game_view.view_left
        HEIGHT = (CONSTANTS.SCREEN_HEIGHT + self.game_view.view_bottom) - self.game_view.view_bottom

        arcade.set_viewport(0, WIDTH - 1, 0, HEIGHT - 1)
        
        # draw an orange filter over him
        arcade.draw_lrtb_rectangle_filled(left=self.game_view.view_left,
                                          right= CONSTANTS.SCREEN_WIDTH + self.game_view.view_left,
                                          top=CONSTANTS.SCREEN_HEIGHT + self.game_view.view_bottom,
                                          bottom=self.game_view.view_bottom,
                                          color=arcade.color.ORANGE + (200,))

        arcade.draw_text("PAUSED", WIDTH/2, HEIGHT/2+50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Press Esc. to return",
                         WIDTH/2,
                         HEIGHT/2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
                      
        arcade.draw_text("Press Enter to reset",
                         WIDTH/2,
                         HEIGHT/2-30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        """Determines what happenes next based on what button is pressed"""
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:  # reset game
            game = GameView()
            game.setup()
            self.window.show_view(game)

class FinishView(arcade.View):
    """ View to show when game is over """

    #wait for key to be pressed to continue
    def wait_for_key(self, key, _modifiers):
        if key == arcade.key.ENTER:  # reset game
            game = GameView()
            game.setup()
            self.window.show_view(game)

            
    #flavoring for text
    def __init__(self, game_view, score, killed, game_time):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture("win_screen.jpg")
        self.game_view = game_view
        self.score = score
        self.killed = killed
        self.game_time = game_time
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

        WIDTH = (CONSTANTS.SCREEN_WIDTH + self.game_view.view_left) -  self.game_view.view_left
        HEIGHT = (CONSTANTS.SCREEN_HEIGHT + self.game_view.view_bottom) - self.game_view.view_bottom
        
        arcade.set_viewport(0, WIDTH - 1, 0, HEIGHT - 1)

        self.texture.draw_sized(WIDTH / 2, HEIGHT / 2,
                                WIDTH, HEIGHT)

        arcade.draw_text(f"{self.score}", WIDTH/2, HEIGHT/2-10,arcade.color.GOLD, font_size=40, anchor_x="center")

        arcade.draw_text(f"You killed {self.killed} enemies,\nand completed the game in {round(self.game_time,2)} seconds.", WIDTH/2, HEIGHT/2-110,
                         arcade.color.GOLD, font_size=20, anchor_x="center")

        arcade.draw_text("Press the Space Bar to reset",
                         WIDTH/2,
                         HEIGHT/2-125,
                         arcade.color.GOLD,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.SPACE:  
            game = GameView()
            game.setup()
            self.window.show_view(game)
