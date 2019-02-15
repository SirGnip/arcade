from arcade.sprite import Sprite
from pymunk import Vec2d

class Particle(Sprite):
    # def update(self):
    #     raise NotImplementedError("Particle.update needs to be implemented")
    #
    # def draw(self):
    #     raise NotImplementedError("Particle.draw needs to be implemented")

    def can_reap(self):
        raise NotImplementedError("Particle.can_reap needs to be implemented")


class EternalParticle(Particle):
    def __init__(self, filename, pos: Vec2d, vel: Vec2d, angle: float, change_angle: float, scale: float, alpha: int):
        super().__init__(filename, scale=scale)
        self.center_x = pos.x
        self.center_y = pos.y
        self.change_x = vel.x
        self.change_y = vel.y
        self.angle = angle
        self.change_angle = change_angle
        self.alpha = alpha


PID = 0
class LifetimeParticle(Particle):
    def __init__(self, filename, pos: Vec2d, vel: Vec2d, angle: float, change_angle: float, scale: float, alpha: int, lifetime: float):
        global PID
        super().__init__(filename, scale=scale)
        self.pid = PID
        PID += 1
        self.center_x = pos.x
        self.center_y = pos.y
        self.change_x = vel.x
        self.change_y = vel.y
        self.angle = angle
        self.change_angle = change_angle
        self.alpha = alpha
        self.lifetime_remaining = lifetime

    def update(self):
        super().update()
        self.lifetime_remaining -= 1/60

    def can_reap(self):
        return self.lifetime_remaining < 0.0


class FadeParticle(LifetimeParticle):
    def __init__(self, filename, pos: Vec2d, vel: Vec2d, angle: float, change_angle: float, scale: float, lifetime: float):
        super().__init__(filename, pos, vel, angle, change_angle, scale, 255, lifetime)
        self.lifetime_original = lifetime

    def update(self):
        super().update()
        self.alpha = 255 * max(0, (self.lifetime_remaining / self.lifetime_original))
