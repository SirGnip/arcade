"""
Sprite Collect Coins - demonstrate Actor and ActorList

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_collect_coins
"""

import random
import arcade
import os
from pymunk import Vec2d

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 25

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "EXPERIMENT: Sprite Collect Coins with ActorList Example"


class Actor:
    def update(self):
        raise NotImplemented("Must implement")

    def draw(self):
        raise NotImplemented("Must implement")

    def can_reap(self) -> bool:
        """Allows an Actor to manage its own lifetime"""
        raise NotImplemented("Must implement")

    def kill(self):
        """Mark this actor as dead so that it can be reaped the next time possible.

        This method is not necessary for most Actor-like objects as they usually manage
        their own lifetime via can_reap.  But, kill() it is a common addition if an Actor's
        lifetime needs to be managed or short from an outside client."""
        raise NotImplemented("Must implement")

# monkey patch existing classes to make them Actor-like
arcade.Sprite.can_reap = lambda other_self: None
arcade.SpriteList.can_reap = lambda other_self: None


class ActorList(list, Actor):
    def draw(self):
        for actor in self:
            actor.draw()

    def update(self):
        actors_to_delete = []
        for actor in self:
            actor.update()
            if actor.can_reap():
                actors_to_delete.append(actor)
        for actor_to_del in actors_to_delete:
            self.remove(actor_to_del)

    def draw(self):
        for actor in self:
            actor.draw()

    def can_reap(self) -> bool:
        return all([actor.can_reap() for actor in self])

    def kill(self):
        for actor in self:
            actor.kill()
        self.clear()


class MessageActor(Actor):
    """Display a given message for a fixed amount of time"""
    def __init__(self, x, y, msg):
        self.msg = msg
        self.x = x
        self.y = y
        self.ticks_remaining = 45

    def update(self):
        self.ticks_remaining -= 1

    def draw(self):
        arcade.draw_text(self.msg,
                         self.x, self.y + 40,
                         arcade.color.WHITE, 24, width=SCREEN_WIDTH, align="center",
                         anchor_x="center", anchor_y="center")

    def can_reap(self):
        return self.ticks_remaining <= 0


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None
        self.actors = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.actors = ActorList()
        self.actors.append(self.player_list)
        self.actors.append(self.coin_list)

        # Score
        self.score = 0

        # Set up the player
        # Character image from kenney.nl
        self.player_sprite = arcade.Sprite("images/character.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite("images/coin_01.png", SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.actors.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.actors.update()

        # Generate a list of all sprites that collided with the player.
        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in coins_hit_list:
            self.actors.append(arcade.make_burst_emitter(Vec2d(coin.center_x, coin.center_y), ["images/bumper.png"], 50, 8, 0.25, 0.5, 0.1))
            self.actors.append(MessageActor(coin.center_x, coin.center_y, "You picked up %s" % random.choice(("a coin", "treasure", "money", "loot", "gold", "chedda"))))
            coin.kill()
            self.score += 1


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
