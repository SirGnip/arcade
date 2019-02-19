"""
Particle Systems

Demonstrate how to use the Emitter and Particle classes to create particle systems

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_list_particle_systems
"""
import arcade
import pyglet
from pymunk import Vec2d
import random
import frametime_plotter

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Particle - sprite list class driven"
QUIET_BETWEEN_SPAWNS = 0.25 # time between spawning another particle system
EMITTER_TIMEOUT = 5*60
CENTER_POS = Vec2d(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
BURST_PARTICLE_COUNT = 500
TEXTURE = "images/pool_cue_ball.png"
TEXTURE2 = "images/playerShip3_orange.png"
TEXTURE3 = "images/bumper.png"
TEXTURE4 = "images/wormGreen.png"
TEXTURE5 = "images/meteorGrey_med1.png"
TEXTURE6 = "images/character.png"
TEXTURE7 = "images/boxCrate_double.png"
DEFAULT_SCALE = 0.3
DEFAULT_ALPHA = 32
DEFAULT_PARTICLE_LIFETIME = 3.0
PARTICLE_SPEED_FAST = 1.0
PARTICLE_SPEED_SLOW = 0.3
DEFAULT_EMIT_INTERVAL = 0.003
DEFAULT_EMIT_DURATION = 1.5


def emitter_0():
    """Burst, emit from center, particle lifetime 2 seconds"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterBurst(BURST_PARTICLE_COUNT),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=Vec2d(emitter.center_x, emitter.center_y),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_FAST),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_0.__doc__, e

def emitter_1():
    """Burst, emit from center, particle lifetime 1.0 seconds"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterBurst(BURST_PARTICLE_COUNT),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=Vec2d(emitter.center_x, emitter.center_y),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_FAST),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=1.0
        )
    )
    return emitter_1.__doc__, e

def emitter_2():
    """Burst, emit from center, particle lifetime random in range"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterBurst(BURST_PARTICLE_COUNT),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=Vec2d(emitter.center_x, emitter.center_y),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_FAST),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=random.uniform(DEFAULT_PARTICLE_LIFETIME-1.0, DEFAULT_PARTICLE_LIFETIME)
        )
    )
    return emitter_2.__doc__, e

def emitter_3():
    """Burst, emit in circle"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterBurst(BURST_PARTICLE_COUNT),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=arcade.rand_in_circle(CENTER_POS, 100),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_SLOW),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_3.__doc__, e

def emitter_4():
    """Burst, emit on circle"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterBurst(BURST_PARTICLE_COUNT),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=arcade.rand_on_circle(CENTER_POS, 100),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_SLOW),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_4.__doc__, e

def emitter_5():
    """Burst, emit in rectangle"""
    width, height = 200, 100
    centering_offset = Vec2d(-width/2, -height/2)
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterBurst(BURST_PARTICLE_COUNT),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=arcade.rand_in_rect(CENTER_POS + centering_offset, width, height),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_SLOW),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_5.__doc__, e

def emitter_6():
    """Burst, emit on line"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterBurst(BURST_PARTICLE_COUNT),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=arcade.rand_on_line(Vec2d(0, 0), Vec2d(SCREEN_WIDTH, SCREEN_HEIGHT)),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_SLOW),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_6.__doc__, e

def emitter_7():
    """Burst, emit from center, velocity fixed speed around 360 degrees"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterBurst(BURST_PARTICLE_COUNT // 4),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=CENTER_POS,
            vel=arcade.rand_on_circle(Vec2d.zero(), PARTICLE_SPEED_FAST),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_7.__doc__, e

def emitter_8():
    """Burst, emit from enter, velocity in rectangle"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterBurst(BURST_PARTICLE_COUNT),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=CENTER_POS,
            vel=arcade.rand_in_rect(Vec2d(-2.0, -2.0), 4.0, 4.0),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_8.__doc__, e

def emitter_9():
    """Burst, emit from center, velocity in fixed angle and random speed"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterBurst(BURST_PARTICLE_COUNT // 4),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=CENTER_POS,
            vel=arcade.rand_vec_magnitude(45, 1.0, 4.0),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_9.__doc__, e

def emitter_10():
    """Burst, emit from center, velocity from angle with spread"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterBurst(BURST_PARTICLE_COUNT // 4),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=CENTER_POS,
            vel=arcade.rand_vec_spread_deg(90, 45, 2.0),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_10.__doc__, e

def emitter_11():
    """Burst, emit from center, velocity along a line"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterBurst(BURST_PARTICLE_COUNT // 4),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=CENTER_POS,
            vel=arcade.rand_on_line(Vec2d(-2, 1), Vec2d(2, 1)),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_11.__doc__, e

def emitter_12():
    """Infinite emitting w/ eternal particle"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterInterval(0.005),
        particle_factory=lambda emitter: arcade.EternalParticle(
            filename=TEXTURE,
            pos=Vec2d(emitter.center_x, emitter.center_y),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_FAST),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA
        )
    )
    return emitter_12.__doc__, e

def emitter_13():
    """Interval, emit particle every 0.01 seconds for one second"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=Vec2d(emitter.center_x, emitter.center_y),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_FAST),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_13.__doc__, e

def emitter_14():
    """Interval, emit from center, particle lifetime 1.0 seconds"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=Vec2d(emitter.center_x, emitter.center_y),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_FAST),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=1.0
        )
    )
    return emitter_14.__doc__, e

def emitter_15():
    """Interval, emit from center, particle lifetime random in range"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=Vec2d(emitter.center_x, emitter.center_y),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_FAST),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=random.uniform(DEFAULT_PARTICLE_LIFETIME-1.0, DEFAULT_PARTICLE_LIFETIME)
        )
    )
    return emitter_15.__doc__, e

def emitter_16():
    """Interval, emit in circle"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=arcade.rand_in_circle(CENTER_POS, 100),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_SLOW),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_16.__doc__, e

def emitter_17():
    """Interval, emit on circle"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=arcade.rand_on_circle(CENTER_POS, 100),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_SLOW),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_17.__doc__, e

def emitter_18():
    """Interval, emit in rectangle"""
    width, height = 200, 100
    centering_offset = Vec2d(-width/2, -height/2)
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=arcade.rand_in_rect(CENTER_POS + centering_offset, width, height),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_SLOW),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_18.__doc__, e

def emitter_19():
    """Interval, emit on line"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=arcade.rand_on_line(Vec2d(0, 0), Vec2d(SCREEN_WIDTH, SCREEN_HEIGHT)),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_SLOW),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_19.__doc__, e

def emitter_20():
    """Interval, emit from center, velocity fixed speed around 360 degrees"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=CENTER_POS,
            vel=arcade.rand_on_circle(Vec2d.zero(), PARTICLE_SPEED_FAST),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_20.__doc__, e

def emitter_21():
    """Interval, emit from enter, velocity in rectangle"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=CENTER_POS,
            vel=arcade.rand_in_rect(Vec2d(-2.0, -2.0), 4.0, 4.0),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_21.__doc__, e

def emitter_22():
    """Interval, emit from center, velocity in fixed angle and speed"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL * 8, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=CENTER_POS,
            vel=Vec2d(1.0, 1.0),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_22.__doc__, e

def emitter_23():
    """Interval, emit from center, velocity in fixed angle and random speed"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL * 8, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=CENTER_POS,
            vel=arcade.rand_vec_magnitude(45, 1.0, 4.0),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_23.__doc__, e

def emitter_24():
    """Interval, emit from center, velocity from angle with spread"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=CENTER_POS,
            vel=arcade.rand_vec_spread_deg(90, 45, 2.0),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_24.__doc__, e

def emitter_25():
    """Interval, emit from center, velocity along a line"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=CENTER_POS,
            vel=arcade.rand_on_line(Vec2d(-2, 1), Vec2d(2, 1)),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_25.__doc__, e

def emitter_26():
    """Interval, emit particles every 0.4 seconds and stop after emitting 5"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithCount(0.4, 5),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=Vec2d(emitter.center_x, emitter.center_y),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_FAST),
            angle=0,
            change_angle=0,
            scale=0.6,
            alpha=128,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_26.__doc__, e

def emitter_27():
    """random particle textures"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL*5, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=random.choice((TEXTURE, TEXTURE2, TEXTURE3)),
            pos=Vec2d(emitter.center_x, emitter.center_y),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_FAST),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=255,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_27.__doc__, e

def emitter_28():
    """random particle scale"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL*5, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=Vec2d(emitter.center_x, emitter.center_y),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_FAST),
            angle=0,
            change_angle=0,
            scale=random.uniform(0.1, 0.8),
            alpha=DEFAULT_ALPHA,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_28.__doc__, e

def emitter_29():
    """random particle alpha"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL*5, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE,
            pos=Vec2d(emitter.center_x, emitter.center_y),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_FAST),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=random.uniform(32, 128),
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_29.__doc__, e

def emitter_30():
    """Constant particle angle"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL*5, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE2,
            pos=Vec2d(emitter.center_x, emitter.center_y),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_FAST),
            angle=45,
            change_angle=0,
            scale=DEFAULT_SCALE,
            alpha=255,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_30.__doc__, e

def emitter_31():
    """animate particle angle"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL*5, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename=TEXTURE2,
            pos=Vec2d(emitter.center_x, emitter.center_y),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_FAST),
            angle=0,
            change_angle=2,
            scale=DEFAULT_SCALE,
            alpha=255,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_31.__doc__, e

def emitter_32():
    """Particles that fade over time"""
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(DEFAULT_EMIT_INTERVAL, DEFAULT_EMIT_DURATION),
        particle_factory=lambda emitter: arcade.FadeParticle(
            filename=TEXTURE,
            pos=Vec2d(emitter.center_x, emitter.center_y),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_FAST),
            angle=0,
            change_angle=0,
            scale=DEFAULT_SCALE,
            lifetime=DEFAULT_PARTICLE_LIFETIME
        )
    )
    return emitter_32.__doc__, e

def emitter_33():
    """Use most features"""
    textures = (TEXTURE, TEXTURE2, TEXTURE3, TEXTURE4, TEXTURE5, TEXTURE6, TEXTURE7)
    e = arcade.Emitter(
        pos=CENTER_POS,
        rate_factory=arcade.EmitterIntervalWithTime(0.01, 1.0),
        particle_factory=lambda emitter: arcade.FadeParticle(
            filename=random.choice(textures),
            pos=Vec2d(emitter.center_x, emitter.center_y),
            vel=arcade.rand_in_circle(Vec2d.zero(), PARTICLE_SPEED_FAST*2),
            angle=random.uniform(0, 360),
            change_angle=random.uniform(-3, 3),
            scale=random.uniform(0.1, 0.8),
            lifetime=random.uniform(1.0, 3.5)
        )
    )
    return emitter_33.__doc__, e


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        # collect particle factory functions
        self.factories = [v for k, v in globals().items() if k.startswith("emitter_")]

        self.emitter_factory_id = -1
        self.label = None
        self.emitter = None
        self.obj = arcade.Sprite("images/bumper.png", 0.2, center_x=0, center_y=15)
        self.obj.change_x = 3
        self.frametime_plotter = frametime_plotter.FrametimePlotter()
        pyglet.clock.schedule_once(self.next_emitter, QUIET_BETWEEN_SPAWNS)

    def next_emitter(self, time_delta):
        self.emitter_factory_id = (self.emitter_factory_id + 1) % len(self.factories)
        print("Changing emitter to {}".format(self.emitter_factory_id))
        self.emitter_timeout = 0
        self.label, self.emitter = self.factories[self.emitter_factory_id]()
        self.frametime_plotter.add_event("spawn {}".format(self.emitter_factory_id))

    def update(self, delta_time):
        if self.emitter:
            self.emitter_timeout += 1
            self.emitter.update()
            if self.emitter.can_reap() or self.emitter_timeout > EMITTER_TIMEOUT:
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
            arcade.draw_text("#{} {}".format(self.emitter_factory_id, self.label),
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20,
                             arcade.color.PALE_GOLD, 20, width=SCREEN_WIDTH, align="center",
                             anchor_x="center", anchor_y="center")
        if self.emitter:
            self.emitter.draw()
            arcade.draw_text("Particles: " + str(len(self.emitter._particles)), 10, 30, arcade.color.PALE_GOLD, 12)


if __name__ == "__main__":
    game = MyGame()
    arcade.run()
    game.frametime_plotter.show()
