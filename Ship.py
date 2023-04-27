from pygame.image import load
from pygame.math import Vector2
from utils import load_sprite, wrap_position


class Ship:
    FORWARD_DIRECTION = Vector2(0, -1)
    ROTATE_SPEED = 3
    ACCELERATION = 0.25

    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.ROTATE_SPEED * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.FORWARD_DIRECTION * self.ACCELERATION

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Player_Ship(Ship):
    def __init__(self, position):
        super().__init__(position, load_sprite("Playership"), Vector2(0))


class NPC_Ship(Ship):
    def __init__(self, position):
        super().__init__(position, load_sprite("NPC"), (0, 0))
