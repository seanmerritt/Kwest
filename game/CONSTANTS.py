# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "KWEST"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = .5
COIN_SCALING = .5
SPRITE_SCALING_LASER = 1
BULLET_SPEED = 10
MY_BULLET_SPEED = 15
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)
SPRITE_SCALING = 0.5
# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 30
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 500
RIGHT_VIEWPORT_MARGIN = 500
BOTTOM_VIEWPORT_MARGIN = 200
TOP_VIEWPORT_MARGIN = 200

PLAYER_START_X = SPRITE_PIXEL_SIZE * TILE_SCALING * 2 + 600
PLAYER_START_Y = SPRITE_PIXEL_SIZE * TILE_SCALING * 1 + 300

## Health Bar 
HEALTHBAR_WIDTH = 25
HEALTHBAR_HEIGHT = 3
HEALTHBAR_OFFSET_Y = 40

HEALTH_NUMBER_OFFSET_X = -10
HEALTH_NUMBER_OFFSET_Y = 45

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

NUMBER_OF_ENEMIES = 5
