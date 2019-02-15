import arcade
from arcade.particle import Particle
from pymunk import Vec2d
from typing import Callable


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
    """Defines rate of spawning for an Emitter. No duration so will emit indefinitely."""
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
        self.center_x = pos.x
        self.center_y = pos.y
        self.rate_factory = rate_factory
        self.particle_factory = particle_factory
        self._particles = arcade.SpriteList(use_spatial_hash=False)

    def _emit(self):
        """Emit one particle. A particle's position is treated relative to the position of the emitter"""
        p = self.particle_factory(self)
        p.center_x = self.center_x + p.center_x
        p.center_y = self.center_y + p.center_y
        self._particles.append(p)

    def _emit_batch_original(self, emit_count):
        idx = 0
        particles = []
        while idx < emit_count:
            particles.append(self.particle_factory(self))
            idx += 1
        self._particles.append_batch(particles)

    def _emit_batch_preallocated_array(self, emit_count):
        """Untested if this actually helps"""
        particles = [None] * emit_count
        for i in range(emit_count):
            particles[i] = self.particle_factory(self)
        self._particles.append_batch(particles)

    _emit_batch = _emit_batch_original

    def update(self):
        emit_count = self.rate_factory.how_many(1/60)
        self._emit_batch(emit_count)
        self._particles.update()
        particles_to_reap = [p for p in self._particles if p.can_reap()]
        # if len(particles_to_reap) > 0:
        #     print("particles to reap {}".format(len(particles_to_reap)))
        if len(particles_to_reap) > 0:
            self._particles.remove_batch(particles_to_reap)

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


########## Convenience functions that return pre-built emitters (A simple way for beginners to use particle systems)
def make_burst_emitter(
        pos: Vec2d,
        filename_or_texture,
        particle_count: int,
        speed: float,  # range? (have speed and speed_range that represents a range around the given speed. If left empty, no range...  Or, "speed" and "speed_max". Just speed is a constant. speed+speed_max defines a range
        particle_lifetime: float,  # range?
        scale: float=1.0
    ):
    """Have a fade:boolean? """
    return arcade.Emitter(
        pos=pos,
        rate_factory=arcade.EmitterBurst(particle_count),
        particle_factory=lambda emitter: arcade.FadeParticle(
            filename_or_texture=filename_or_texture,
            pos=Vec2d.zero(),
            vel=arcade.rand_in_circle(Vec2d.zero(), speed),
            angle=0,
            change_angle=0,
            scale=scale,
            lifetime=particle_lifetime
        )
    )

def make_interval_emitter(
        pos: Vec2d,
        filename_or_texture,
        emit_interval: float,
        emit_duration: float,
        speed: float, # range? (have speed and speed_range that represents a range around the given speed. If left empty, no range...  Or, "speed" and "speed_max". Just speed is a constant. speed+speed_max defines a range
        particle_lifetime: float,  # range?
        scale: float = 1.0
    ):
    return arcade.Emitter(
        pos=pos,
        rate_factory=arcade.EmitterIntervalWithTime(emit_interval, emit_duration),
        particle_factory=lambda emitter: arcade.FadeParticle(
            filename_or_texture=filename_or_texture,
            pos=Vec2d.zero(),
            vel=arcade.rand_on_circle(Vec2d.zero(), speed),
            angle=0,
            change_angle=0,
            scale=scale,
            lifetime=particle_lifetime
        )
    )