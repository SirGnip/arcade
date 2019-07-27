"""
This program shows how to have screens (menu, pause) that layer over a game screen.

This is NOT a construct for beginners, but shows what kind of flexibility is
possible with the WindowWithStates/WindowState system.

The main game logic goes in GameWindow and is a GameWithStates. The individual
"states" are drawn on top of the running game itself, with the GameWindow still
visible below.

The key implementation point is that the GameWindow (which is the Window, not a State)
needs to call the super() of its on_draw(), update(), and on_key_press() methods
to make sure these methods also get called on current_state.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.different_screens_pause_layered
"""

import arcade
import random
import os


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


WIDTH = 800
HEIGHT = 600
TITLE = "Instruction and Layered Game Over Screens Example"
SPRITE_SCALING = 0.5


class MenuState(arcade.WindowState):
    def on_draw(self):
        arcade.draw_xywh_rectangle_filled(0, 0, WIDTH, HEIGHT, (30, 30, 30, 180))
        arcade.draw_text("Menu Screen", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("(click to continue)", WIDTH/2, (HEIGHT/2)-50,
                         arcade.color.BLACK, font_size=25, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        self.parent.set_state(None)


class GameWindow(arcade.WindowWithStates):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.next_state(MenuState)
        arcade.set_background_color(arcade.color.AMAZON)

    def is_paused(self):
        """Pause GameWindow when a State is active (meaning something is being drawn on drop"""
        return self.current_state is not None

    def setup(self):
        self.player_sprite = arcade.Sprite("images/character.png", SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_sprite.velocity = [3, 3]

    def on_draw(self):
        arcade.start_render()

        # Draw all the sprites.
        self.player_sprite.draw()

        # Show tip to pause screen
        if not self.is_paused():
            arcade.draw_text("Press Esc. to pause",
                             WIDTH/2,
                             HEIGHT-100,
                             arcade.color.BLACK,
                             font_size=20,
                             anchor_x="center")

        super().on_draw()

    def update(self, delta_time):
        if self.is_paused():
            return

        # Call update on all sprites
        self.player_sprite.update()

        # Bounce off the edges
        if self.player_sprite.left < 0 or self.player_sprite.right > WIDTH:
            self.player_sprite.change_x *= -1
        if self.player_sprite.bottom < 0 or self.player_sprite.top > HEIGHT:
            self.player_sprite.change_y *= -1

        super().update(delta_time)

    def on_key_press(self, key, modifiers):
        if not self.is_paused():
            if key == arcade.key.ESCAPE:
                self.next_state(PauseState)
                return

        super().on_key_press(key, modifiers)


class PauseState(arcade.WindowState):
    def on_draw(self):
        arcade.draw_xywh_rectangle_filled(0, 0, WIDTH, HEIGHT, (128, 0, 0, 128))
        arcade.draw_text("PAUSED", WIDTH/2, HEIGHT/2+50,
                         arcade.color.ORANGE, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Press Esc. to return",
                         WIDTH/2,
                         HEIGHT/2,
                         arcade.color.ORANGE,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press Enter to reset",
                         WIDTH/2,
                         HEIGHT/2-30,
                         arcade.color.ORANGE,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.parent.set_state(None)
        elif key == arcade.key.ENTER:  # reset game
            self.parent.set_state(None)
            self.parent.setup()


def main():
    app = GameWindow(WIDTH, HEIGHT, TITLE)
    app.setup()
    arcade.run()


if __name__ == "__main__":
    main()
