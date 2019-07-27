"""
This program shows how to have a pause screen without resetting the game.

Your game window will derive from WindowWithStates and each screen in your
game will need to have its own class derived from WindowState, which has
their own draw, update, and window event methods.  To switch a screen,
simply use the MyWindow.next_state() function and pass it the ClassName
of the screen you want to switch to.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.instruction_and_game_over_screens
"""

import arcade
import random
import os


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


WIDTH = 800
HEIGHT = 600
SPRITE_SCALING = 0.5


class MyWindow(arcade.WindowWithStates):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.next_state(MenuScreen)


class MenuScreen(arcade.WindowState):
    def begin(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Menu Screen", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        self.parent.next_state(GameScreen)


class GameScreen(arcade.WindowState):
    def setup(self):
        self.player_sprite = arcade.Sprite("images/character.png", SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_sprite.velocity = [3, 3]

    def begin(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        arcade.start_render()
        # Draw all the sprites.
        self.player_sprite.draw()

        # Show tip to pause screen
        arcade.draw_text("Press Esc. to pause",
                         WIDTH/2,
                         HEIGHT-100,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def update(self, delta_time):
        # Call update on all sprites
        self.player_sprite.update()

        # Bounce off the edges
        if self.player_sprite.left < 0 or self.player_sprite.right > WIDTH:
            self.player_sprite.change_x *= -1
        if self.player_sprite.bottom < 0 or self.player_sprite.top > HEIGHT:
            self.player_sprite.change_y *= -1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.parent.next_state(PauseScreen)


class PauseScreen(arcade.WindowState):
    def begin(self):
        arcade.set_background_color(arcade.color.ORANGE)

    def on_draw(self):
        arcade.start_render()
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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.parent.next_state(GameScreen)
        elif key == arcade.key.ENTER:  # reset game
            self.parent.next_state(GameScreen, reset=True)


def main():
    MyWindow(WIDTH, HEIGHT, "Instruction and Game Over Screens Example")
    arcade.run()


if __name__ == "__main__":
    main()