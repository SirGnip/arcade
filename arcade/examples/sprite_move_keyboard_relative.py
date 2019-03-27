"""
Move Sprite With Keyboard - relative

EXPERIMENT - see two different types of relative motion on a Sprite

Artwork from http://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_keyboard

NOTES ABOUT EXPERIMENT:
- having the two "modes" of relative motion is confusing.  Plus, I don't know how much performance penalty there is.
    - Maybe have a subclass that adds the "continuous-relative motion"?
    - Maybe have a flag that toggles it on/off?
    - Maybe have a way to inject (callbakcs) new motion behavior into a sprite?
    - Maybe don't sweat the complexity, name the methods well, and just implement both?
"""

import arcade
import os

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Move Sprite with Keyboard Example - relative motion"

MOVEMENT_SPEED = 5


class Player(arcade.Sprite):

    def update(self):
        super().update()
        # self.center_x += self.change_x
        # self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player("images/character.png", SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.player_list.draw()

    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.player_list.update()
        p = self.player_sprite
        # print("{} {} {} {}".format(p.center_x, p.center_y, p.angle, p.change_angle))

    def on_key_press_simple(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP:
            self.player_sprite.forward(10)
        elif key == arcade.key.DOWN:
            self.player_sprite.backward(10)
        elif key == arcade.key.LEFT:
            self.player_sprite.turn_left(30)
        elif key == arcade.key.RIGHT:
            self.player_sprite.turn_right(30)

    def on_key_release_simple(self, key, modifiers):
        """Called when the user releases a key. """
        pass

    def on_key_press_motion(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.move_fwd(2)
        elif key == arcade.key.DOWN:
            self.player_sprite.move_bak(2)
        elif key == arcade.key.LEFT:
            self.player_sprite.move_left(3)
        elif key == arcade.key.RIGHT:
            self.player_sprite.move_right(3)

    def on_key_release_motion(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.move_stop()
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0

    # flip between two types of relative motion "simple" and "in-motion"
    if True:
    # if False:
        on_key_press = on_key_press_simple
        on_key_release = on_key_release_simple
    else:
        on_key_press = on_key_press_motion
        on_key_release = on_key_release_motion

def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
