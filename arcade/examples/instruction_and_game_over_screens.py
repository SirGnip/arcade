"""
This program shows how to use the WindowWithStates/WindowState to:
  * Have one or more instruction screens
  * Show a 'Game over' text and halt the game
  * Allow the user to restart the game

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.instruction_and_game_over_screens
"""

import arcade
import random
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPRITE_SCALING = 0.5
SCREEN_TITLE = "Instruction and Game Over Screens Example"


class MyGame(arcade.WindowWithStates):
    """
    Main application class.
    """

    def __init__(self, screen_width, screen_height, title):
        """ Constructor """
        # Call the parent constructor. Required and must be the first line.
        super().__init__(screen_width, screen_height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # shared data
        self.time_taken = None

        # Start 'state' will be showing the first page of instructions.
        self.next_state(MenuScreen)


class MenuScreen(arcade.WindowState):
    def begin(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Menu Screen", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        self.parent.next_state(InstructionScreen)


class InstructionScreen(arcade.WindowState):
    def begin(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)
        self.screen_name = "Instructions"

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(f"{self.screen_name} Screen", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        self.parent.next_state(GameScreen)


class GameScreen(arcade.WindowState):
    def setup(self):
        self.parent.time_taken = 0
        arcade.set_background_color(arcade.color.AMAZON)

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player_sprite = arcade.Sprite("images/character.png", SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        for i in range(5):

            # Create the coin instance
            coin = arcade.Sprite("images/coin_01.png", SPRITE_SCALING / 3)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)

        # Don't show the mouse cursor
        arcade.get_window().set_mouse_visible(False)

    def on_draw(self):
        arcade.start_render()
        # Draw all the sprites.
        self.player_list.draw()
        self.coin_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def update(self, delta_time):
        self.parent.time_taken += delta_time

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.coin_list.update()
        self.player_list.update()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the
        # score.
        for coin in hit_list:
            coin.kill()
            self.score += 1

        # If we've collected all the games, then move to a "GAME_OVER"
        # state.
        if len(self.coin_list) == 0:
            arcade.get_window().set_mouse_visible(True)
            self.parent.next_state(GameOverScreen)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y


class GameOverScreen(arcade.WindowState):
    def begin(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        """
        Draw "Game over" across the screen.
        """
        arcade.draw_text("Game Over", 240, 400, arcade.color.WHITE, 54)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.WHITE, 24)

        time_taken_formatted = f"{round(self.parent.time_taken, 2)} seconds"
        arcade.draw_text(f"Time taken: {time_taken_formatted}",
                         SCREEN_WIDTH / 2,
                         200,
                         arcade.color.GRAY,
                         font_size=15,
                         anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        self.parent.next_state(GameScreen, reset=True)


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
