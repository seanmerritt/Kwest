"""
This program shows how to:
  * Have one or more instruction screens
  * Show a 'Game over' text and halt the game
  * Allow the user to restart the game

Make a separate class for each view (screen) in your game.
The class will inherit from arcade.View. The structure will
look like an arcade.Window as each view will need to have its own draw,
update and window event methods. To switch a view, simply create a view
with `view = MyView()` and then use the view.show() method.

This example shows how you can set data from one View on another View to pass data
around (see: time_taken), or you can store data on the Window object to share data between
all Views (see: total_score).

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.view_instructions_and_game_over.py
"""

import arcade
import random
import os
from game.director import GameView
from game import CONSTANTS


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)



class MenuView(arcade.View):
    """The first thing you see once you start the game
    Methods in Class:
    - __init__(self)
    - on_show(self)
    - on_draw(self)
    - on_mouse_press(self, _x, _y, _button, _modifiers)
    """
    def __init__(self):
        """Constructor, pulls from other codes"""
        super().__init__()
        
    def on_show(self):
        """Sets background color"""
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """Displays text"""
        arcade.start_render()
        arcade.draw_text("KWEST!", CONSTANTS.SCREEN_WIDTH/2, CONSTANTS.SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", CONSTANTS.SCREEN_WIDTH/2, CONSTANTS.SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Switches to Instruction screen after mouse click"""
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    """Tells the player how to play the game. Diplays controls, instructions, and story
    Methods in Class:
    - __init__(self)
    - on_show(self)
    - on_draw(self)
    - on_mouse_press(self, _x, _y, _button, _modifiers)
    """
    def __init__(self):
        """Constructor, pull from other codes"""
        super().__init__()

    def on_show(self):
        """Shows background for instruction page"""
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        """Displays text for instruction page"""
        arcade.start_render()
        arcade.draw_text("Instructions", CONSTANTS.SCREEN_WIDTH/2, CONSTANTS.SCREEN_HEIGHT/3* 2,
                         arcade.color.BLACK, font_size=25, anchor_x="center")
        arcade.draw_text("Use the arrow keys to move and the space bar to shoot (after you find the power gem). \nPress esc to pause at any time. \nClick to advance",
                         CONSTANTS.SCREEN_WIDTH/2, (CONSTANTS.SCREEN_HEIGHT/3 *2 )- 80,
                         arcade.color.BLACK, font_size=15, anchor_x="center")
        arcade.draw_text("Story",
                         CONSTANTS.SCREEN_WIDTH/2, (CONSTANTS.SCREEN_HEIGHT/3 *2)-120,
                         arcade.color.BLACK, font_size=25, anchor_x="center")
        arcade.draw_text("A long time ago in a Galaxy far, far away . . .\nSome random aliens decided that they wanted El Dorado’s greatest treasure, the “Golden Man,” whatever the heck that’s supposed to be.\nAfter lightyears of travel, those aliens have finally reached Earth and are on the hunt.\nBut if anyone’s going to steal some giant golden man from some old gold city, it’s going to be one of our own that LIVES HERE, thank you VERY much.\nWhat’s that?\nI don’t CARE if we thought it was just a legend until now.\nYeah, yeah, okay, I know – we haven’t been able to find it after centuries of looking, but we’re a lot more motivated now AREN’T WE?\nSorry, you’ll have to speak up.\nOh. Why send you? Um. Well – We heard you were like, REALLY into Drake’s Fortune from the Uncharted series.\nDon’t think about it too much, ‘kay?\n. . . Just shut up and go find the stupid gold statue or whatever already.", 
                         CONSTANTS.SCREEN_WIDTH/2, 
                         (CONSTANTS.SCREEN_HEIGHT/3 *2)-250,
                         arcade.color.BLACK, font_size=10, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Starts game after mouse is clicked"""
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameOverView(arcade.View):
    """Screen for when player dies
    Methods in Classes:
    - __init__(self)
    - on_show(self)
    - on_draw(self)
    - on_mouse_press(self, _x, _y, _button, _modifiers)
    """
    def __init__(self):
        """Constructor, pulls from other code and starts time at zero seconds"""
        super().__init__()
        self.time_taken = 0

    def on_show(self):
        """Sets up backdrop for game over screen"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        """
        Draw "Game over" across the screen.
        """
        arcade.draw_text("Game Over", 240, 400, arcade.color.WHITE, 54)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.WHITE, 24)

        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        arcade.draw_text(f"Time taken: {time_taken_formatted}",
                         CONSTANTS.SCREEN_WIDTH/2,
                         200,
                         arcade.color.GRAY,
                         font_size=15,
                         anchor_x="center")

        output_total = f"Total Score: {self.window.total_score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """restarts game after mouse is clicked"""
        game_view = GameView()
        self.window.show_view(game_view)
