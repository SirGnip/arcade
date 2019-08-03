"""
This program shows how to have a pause screen without resetting the game.

Make a seperate class for each view (screen) in your game.
The class will inherit from arcade.View. The structure will
look like an arcade.Window as each view will need to have its own draw,
update and window event methods. To switch a view, simply create a view
with `view = MyView()` and then use the view.show() method.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.different_screens_pause
"""

import arcade
import os


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


WIDTH = 800
HEIGHT = 600
SPRITE_SCALING = 0.5


class MenuView(arcade.View):
    def on_draw(self):
        arcade.draw_xywh_rectangle_filled(0, 0, WIDTH, HEIGHT, arcade.color.WHITE)
        arcade.draw_text("Menu Screen", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance.", WIDTH/2, HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        self.parent.show_view(None)  # have just the GameWindow visible with no View on top


class GameWindow(arcade.WindowWithViews):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.AMAZON)
        self.player_sprite = arcade.Sprite("images/character.png", SPRITE_SCALING)

    def on_show(self):
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_sprite.velocity = [3, 3]

    def is_paused(self):
        """Return if game is in a paused state. Used to determine when a View is being drawn on top of GameWindow"""
        return self.current_view is not None

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

    def on_key_press(self, key, modifiers):
        if not self.is_paused():
            if key == arcade.key.ESCAPE:
                self.show_view(PauseView())
                return

        super().on_key_press(key, modifiers)


class PauseView(arcade.View):
    def on_draw(self):
        # draw an orange filter over GameWindow
        arcade.draw_xywh_rectangle_filled(bottom_left_x=0,
                                          bottom_left_y=0,
                                          width=WIDTH,
                                          height=HEIGHT,
                                          color=(*arcade.color.ORANGE, 200))

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
            self.parent.show_view(None) # have just the GameWindow visible with no View on top
        elif key == arcade.key.ENTER:  # reset game
            self.parent.show_view(None) # have just the GameWindow visible with no View on top
            self.parent.on_show()


def main():
    window = GameWindow(WIDTH, HEIGHT, "Instruction and Game Over Views Example")
    window.show_view(MenuView())
    arcade.run()


if __name__ == "__main__":
    main()
