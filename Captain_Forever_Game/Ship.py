from pygame.image import load
from pygame.math import Vector2

# from captain_forever.utils import load_sprite, wrap_position


def wrap_position(position, surface):
    """
    Ensuring that the object would not fall off screen
    """
    x = position.x % surface.get_width()
    y = position.y % surface.get_height()
    return pygame.Vector2(x, y)


class Ship:
    FORWARD_DIRECTION = pygame.Vector2(0, -1)
    ROTATE_SPEED = 3
    ACCELERATION = 0.25

    def __init__(self, position, sprite, velocity):
        self.position = pygame.Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = pygame.Vector2(velocity)

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.ROTATE_SPEED * sign
        self.FORWARD_DIRECTION.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.FORWARD_DIRECTION * self.ACCELERATION

    def draw(self, surface):
        blit_position = self.position - pygame.Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius
