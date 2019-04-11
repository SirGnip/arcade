"""
Demonstrate multiple viewports

Render the same scene in two different views. Also, be able to dynamically flip between
a single view and multiple views.
"""

import arcade
import os
from pyglet import gl


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Demonstrate Splitscreen"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.AMAZON)

        self.split_on = False

        self.emitter = arcade.make_interval_emitter(
            center_xy=(150, 150),
            filenames_and_textures=["images/character.png"],
            emit_interval=0.4,
            emit_duration=60.0,
            particle_speed=1.0,
            particle_lifetime_min=6.0,
            particle_lifetime_max=7.0
        )

    def _make_view(self, xpos, ypos):
        arcade.set_viewport(-xpos,               # x start position of window into world
                            SCREEN_WIDTH-xpos,   # width of window into world
                            -ypos,               # y start position of window into world
                            SCREEN_HEIGHT-ypos)  # height of window into world
        gl.glScissor(xpos, ypos, 350, 350)       # only show pixels within x,y,width,height, these coordinates are in screen-space

    def on_draw(self):
        # clear full screen
        arcade.set_background_color((0, 100, 0))
        arcade.start_render()

        if self.split_on:
            gl.glEnable(gl.GL_SCISSOR_TEST)

            # Viewport #1
            self._make_view(25, 225)
            arcade.set_background_color((100, 0, 0))
            self.draw_scene()

            # # Viewport #2
            self._make_view(425, 25)
            arcade.set_background_color((0, 0, 100))
            self.draw_scene()

            gl.glDisable(gl.GL_SCISSOR_TEST)
        else:
            # fullscreen viewport
            self._make_view(0, 0)
            self.draw_scene()

    def draw_scene(self):
        arcade.start_render()
        self.emitter.draw()
        arcade.draw_text("Press any key to toggle multi-view", 10, 10, arcade.color.WHITE, 20)

    def update(self, delta_time):
        self.emitter.update()

    def on_key_press(self, symbol: int, modifiers: int):
        self.split_on = not self.split_on


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
