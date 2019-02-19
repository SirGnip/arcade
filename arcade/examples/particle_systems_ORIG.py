"""
Particle Systems

Demonstrate how to use the Emitter and Particle classes to create particle systems

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_list_particle_systems
"""
import arcade
import pyglet
import random
from pymunk import Vec2d
import frametime_plotter

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Particle - sprite list class driven"
QUIET_BETWEEN_SPAWNS = 0.25 # time between spawning another particle system


def emitter1():
    """basic burst emitter"""
    return emitter1.__doc__, arcade.Emitter(
        Vec2d(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
        arcade.EmitterBurst(3000),
        lambda emitter: arcade.LifetimeParticle("images/pool_cue_ball.png",
                                         Vec2d(emitter.center_x, emitter.center_y),
                                         arcade.rand_in_circle(Vec2d.zero(), 2),
                                         0,
                                         0,
                                         0.3,
                                         32, 2.0))

def emitter1A():
    """basic burst emitter with variable lifetimes"""
    return emitter1A.__doc__, arcade.Emitter(
        Vec2d(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
        arcade.EmitterBurst(3000),
        lambda emitter: arcade.LifetimeParticle("images/pool_cue_ball.png",
                                         Vec2d(emitter.center_x, emitter.center_y),
                                         arcade.rand_in_circle(Vec2d.zero(), 2),
                                         0,
                                         0,
                                         0.3,
                                         32,
                                         random.uniform(1.5, 5.0)))


"""
constant speed in constant diretion        Vec2d(5, 5)
constant speed in 360 direction            rand_on_circle(center, 5)
constant speed in partial sweep direction  rand_vec_spread_deg(90, 45, 5)
random speed in constant direction         v.angle=90 v.length=random.uniform(1, 5)
random speed in 360 direction              rand_in_circle(center, 5)
random speed in partial sweep direction    rand_vec_spread_deg(90, 45, rand)
"""
def emitter1a():
    """Spawn at angle with spread"""
    center = Vec2d(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # pos_func = lambda: rand_in_rect(center, 300, 100)
    vec_func = lambda: arcade.rand_vec_spread_deg(90, 45, random.uniform(0.1, 2.0))
    return emitter1a.__doc__, arcade.Emitter(
        center,
        arcade.EmitterBurst(500),
        lambda emitter: arcade.LifetimeParticle("images/pool_cue_ball.png",
                                         center,
                                         vec_func(),
                                         0,
                                         0,
                                         0.3,
                                         32, 3.0))

def emitter1b():
    """Spawn in circle"""
    center = Vec2d(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    pos_func = lambda: arcade.rand_in_circle(center, 100)
    return emitter1b.__doc__, arcade.Emitter(
        center,
        arcade.EmitterBurst(500),
        lambda emitter: arcade.LifetimeParticle("images/pool_cue_ball.png",
                                         pos_func(),
                                         Vec2d(random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)),
                                         0,
                                         0,
                                         0.3,
                                         32, 3.0))

def emitter1c():
    """spawn on line"""
    center = Vec2d(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    pos_func = lambda: arcade.rand_on_line(Vec2d(0, 0), Vec2d(SCREEN_WIDTH, SCREEN_HEIGHT))
    return emitter1c.__doc__, arcade.Emitter(
        center,
        arcade.EmitterBurst(500),
        lambda emitter: arcade.LifetimeParticle("images/pool_cue_ball.png",
                                         pos_func(),
                                         Vec2d(random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)),
                                         0,
                                         0,
                                         0.3,
                                         32, 3.0))

def emitter1d():
    """spawn on circle"""
    center = Vec2d(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    pos_func = lambda: arcade.rand_on_circle(center, 200)
    return emitter1d.__doc__, arcade.Emitter(
        center,
        arcade.EmitterBurst(500),
        lambda emitter: arcade.LifetimeParticle("images/pool_cue_ball.png",
                                         pos_func(),
                                         Vec2d(random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)),
                                         0,
                                         0,
                                         0.3,
                                         32, 3.0))

def emitter2():
    """spawn only 5"""
    return emitter2.__doc__, arcade.Emitter(
        Vec2d(200, 200),
        arcade.EmitterIntervalWithCount(0.3, 5),
        lambda src_emitter: arcade.LifetimeParticle("images/bumper.png",
                                             Vec2d(src_emitter.center_x, src_emitter.center_y),
                                             Vec2d(random.uniform(-1, 1), random.uniform(-1, 1)),
                                             0,
                                             2,
                                             0.3,
                                             255, 2.0))

def emitter3():
    """spawn and fade"""
    return emitter3.__doc__, arcade.Emitter(
        Vec2d(200, 200),
        arcade.EmitterIntervalWithTime(.03, 1.5),
        lambda emitter: arcade.FadeParticle("images/bumper.png",
                                     Vec2d(emitter.center_x, emitter.center_y),
                                     Vec2d(random.uniform(-1, 1), random.uniform(-1, 1)),
                                     0,
                                     0,
                                     0.3,
                                     1.0))

def emitter4():
    """random images"""
    center = Vec2d(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    image_chooser = lambda: random.choice(("images/bumper.png", "images/boxCrate_double.png", "images/wormGreen.png", "images/meteorGrey_big2.png"))
    vel_func = lambda: arcade.rand_on_circle(Vec2d.zero(), 1)
    return emitter4.__doc__, arcade.Emitter(
        center,
        arcade.EmitterIntervalWithTime(.05, 5.0),
        lambda emitter: arcade.FadeParticle(image_chooser(),
                                     Vec2d(emitter.center_x, emitter.center_y),
                                     vel_func(),
                                     0,
                                     random.uniform(-2, 2),
                                     random.uniform(0.1, 0.6),
                                     6.0))


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.factories = [
            emitter1,
            emitter1A,
            emitter1a,
            emitter1b,
            emitter1c,
            emitter1d,
            emitter2,
            emitter3,
            emitter4,
        ]
        self.emitter_factory_id = 0
        self.label = None
        self.emitter = None
        self.obj = arcade.Sprite("images/bumper.png", 0.2, center_x=0, center_y=15)
        self.obj.change_x = 3
        self.frametime_plotter = frametime_plotter.FrametimePlotter()
        # self.next_emitter(None)
        pyglet.clock.schedule_once(self.next_emitter, QUIET_BETWEEN_SPAWNS)

    def next_emitter(self, time_delta):
        print("Changing emitter to {}".format(self.emitter_factory_id))
        self.label, self.emitter = self.factories[self.emitter_factory_id]()
        self.frametime_plotter.add_event("spawn {}".format(self.emitter_factory_id))
        self.emitter_factory_id = (self.emitter_factory_id + 1) % len(self.factories)

    def update(self, delta_time):
        if self.emitter:
            self.emitter.update()
            if self.emitter.can_reap():
                self.label = None
                self.frametime_plotter.add_event("reap")
                pyglet.clock.schedule_once(self.next_emitter, QUIET_BETWEEN_SPAWNS)
                self.emitter = None
        self.obj.update()
        if self.obj.center_x > SCREEN_WIDTH:
            self.obj.center_x = 0
        self.frametime_plotter.end_frame(delta_time)

    def on_draw(self):
        arcade.start_render()
        self.obj.draw()
        if self.label:
            arcade.draw_text(self.label,
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20,
                             arcade.color.PALE_GOLD, 24, width=SCREEN_WIDTH, align="center",
                             anchor_x="center", anchor_y="center")
        if self.emitter:
            self.emitter.draw()


if __name__ == "__main__":
    game = MyGame()
    arcade.run()
    game.frametime_plotter.show()
