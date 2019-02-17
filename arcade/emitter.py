import arcade
from arcade.particle import Particle
import math
import random
from pymunk import Vec2d
from typing import Callable


########## Util functions
def lerp(v1: float, v2: float, u: float) -> float:
    """linearly interpolate between two values"""
    return v1 + ((v2 - v1) * u)

def vec_lerp(v1: Vec2d, v2: Vec2d, u: float) -> Vec2d:
    return Vec2d(
        lerp(v1.x, v2.x, u),
        lerp(v1.y, v2.y, u)
    )

def rand_in_rect(pos: Vec2d, width: float, height: float) -> Vec2d:
    return Vec2d(
        random.uniform(pos.x, pos.x + width),
        random.uniform(pos.y, pos.y + height)
    )

def rand_in_circle(center: Vec2d, radius: float) -> Vec2d:
    """Generate a point in a circle, or can think of it as a vector pointing a random direction with a random magnitude <= radius
    Reference: http://stackoverflow.com/a/30564123
    Note: This algorithm returns a higher concentration of points around the center of the circle"""
    # random angle
    angle = 2 * math.pi * random.random()
    # random radius
    r = radius * random.random()
    # calculating coordinates
    return Vec2d(
        r * math.cos(angle) + center.x,
        r * math.sin(angle) + center.y
    )

def rand_on_circle(center: Vec2d, radius: float) -> Vec2d:
    """Note: by passing a random value in for float, you can achieve what rand_in_circle() does"""
    angle = 2 * math.pi * random.random()
    return Vec2d(
        radius * math.cos(angle) + center.x,
        radius * math.sin(angle) + center.y
    )

def rand_on_line(pos1: Vec2d, pos2: Vec2d) -> Vec2d:
    u = random.uniform(0.0, 1.0)
    return vec_lerp(pos1, pos2, u)

def rand_angle_360_deg():
    return random.uniform(0.0, 360.0)

def rand_angle_spread_deg(angle: float, half_angle_spread: float):
    s = random.uniform(-half_angle_spread, half_angle_spread)
    return angle + s

def rand_vec_spread_deg(angle: float, half_angle_spread: float, length: float):
    a = rand_angle_spread_deg(angle, half_angle_spread)
    v = Vec2d().ones()
    v.length = length
    v.angle_degrees = a
    return v


########## Classes a client uses to configure an Emitter. Controls the rate of emitting and the duration of emitting
class EmitterController:
    def how_many(self, delta_time: float) -> int:
        raise NotImplemented("EmitterRate.how_many must be implemented")

    def is_complete(self):
        raise NotImplemented("EmitterRate.is_complete must be implemented")


class EmitterBurst(EmitterController):
    """Emits particles in one burst"""
    def __init__(self, count: int):
        self._is_complete = False
        self._count = count

    def how_many(self, delta_time: float) -> int:
        if not self._is_complete:
            self._is_complete = True
            return self._count
        return 0

    def is_complete(self):
        return True


# TODO: reduce code duplication of "carryover_time" logic
class EmitterInterval(EmitterController):
    """Defines rate of spawning for an Emitter. No duration."""
    def __init__(self, emit_interval: float):
        self._emit_interval = emit_interval
        self._carryover_time = 0.0

    def how_many(self, delta_time: float) -> int:
        self._carryover_time += delta_time
        emit_count = 0
        while self._carryover_time >= self._emit_interval:
            self._carryover_time -= self._emit_interval
            emit_count += 1
        return emit_count

    def is_complete(self):
        return False


class EmitterIntervalWithCount(EmitterController):
    """Emits particles at the given interval, ending after emitting the given number of particles"""
    def __init__(self, emit_interval: float, particle_count: int):
        self._emit_interval = emit_interval
        self._count_remaining = particle_count
        self._carryover_time = 0.0

    def how_many(self, delta_time: float) -> int:
        self._carryover_time += delta_time
        emit_count = 0
        while self._count_remaining > 0 and self._carryover_time >= self._emit_interval:
            self._carryover_time -= self._emit_interval
            emit_count += 1
            self._count_remaining -= 1
        return emit_count

    def is_complete(self):
        return self._count_remaining <= 0


class EmitterIntervalWithTime(EmitterController):
    """Emits particles at the given interval, ending after given number of seconds"""
    def __init__(self, emit_interval: float, lifetime: float):
        self._emit_interval = emit_interval
        self._carryover_time = 0.0
        self._lifetime = lifetime

    def how_many(self, delta_time: float) -> int:
        # TODO: handle the imprecision of low particles_per_sec
        if self._lifetime <= 0.0:
            return 0
        self._lifetime -= delta_time
        self._carryover_time += delta_time
        emit_count = 0
        while self._carryover_time >= self._emit_interval:
            self._carryover_time -= self._emit_interval
            emit_count += 1
        return emit_count

    def is_complete(self):
        return self._lifetime <= 0



########## Emitter
class Emitter:
    def __init__(self, pos: Vec2d, rate_factory: EmitterController, particle_factory: Callable[["Emitter"], Particle]):
        # Note Self-reference with type annotations: https://www.python.org/dev/peps/pep-0484/#the-problem-of-forward-declarations
        # super().__init__(filename=None, center_x=x, center_y=y)
        self.center_x = pos.x
        self.center_y = pos.y
        self.rate_factory = rate_factory
        self.particle_factory = particle_factory
        self._particles = arcade.SpriteList(use_spatial_hash=False)

    def _emit(self):
        p = self.particle_factory(self)
        self._particles.append(p)

    def update(self):
        emit_count = self.rate_factory.how_many(1/60)
        for _ in range(emit_count):
            self._emit()
        self._particles.update()
        particles_to_reap = [p for p in self._particles if p.can_reap()]
        # if len(particles_to_reap) > 0:
        #     print("particles to reap {}".format(len(particles_to_reap)))
        for dead_particle in particles_to_reap:
            dead_particle.kill()

        # Need to iterate and get list of dead particles. then delete those from sprite list (while not iterating over sprite list.
        # sweep and update all particles. then get the list of those that are ready to be reaped (do i return this as part of update() so that I don't have to iterate twice?). Or is this early optimization?
        # Crate an "Actor" interface and have particle (and Emitter?) implement it.

        """each sprite can be in multiple sprite lists
        """

    def draw(self):
        # print("Particles: draw {}".format(len(self._particles)))
        self._particles.draw()

    def can_reap(self):
        return self.rate_factory.is_complete() and len(self._particles) <= 0
