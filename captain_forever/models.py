import pygame
from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import get_random_velocity, load_sprite, wrap_position

# Because pygame has inverted y axis, this vector points UP (used for calculations)
UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity):
        """
        initializes a GameObject instance
        """
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        """
        draws the game object onto a surface at its current position
        """
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        """
        moves game objects and wraps screen-exiting objects back on
        """
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        """
        Returns whether a collision has occured between two game objects (bool)
        """
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Ship(GameObject):
    """
    represents player and npc ship instances

    Constants: 
        MANEUVERABILITY: int, degrees per second a ship can turn
        ACCELERATION: float, rate of cartesian transform velocity change

    Args: 
        position: tuple of ints, position on surface to draw the ship

    Methods: 
        rotate: rotates the ship by MANEUVERABILITY degrees
        draws the ship on a surface with an applied rotation

    """
    MANEUVERABILITY = 3
    ACCELERATION = .25
    BULLET_SPEED = 3

    def __init__(self, position, create_bullet_callback):
        """
        initializes Ship (NPC and player) and bullet callbacks
        """
        # creates callback for game to access bullets
        self.create_bullet_callback = create_bullet_callback

        # initialize unit vector upwards initial direction
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("player_ship"), Vector2(0))

    def rotate(self, clockwise=True):
        """
        rotate the direction vector of the ship by MANEUVERABILITY degrees
        """
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        """
        increases velocity of the ship in the direction it is facing
        """
        self.velocity += self.direction * self.ACCELERATION

    def shoot(self):
        """
        creates a bullet shooting in the direction of the ship from its position
        """
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)

    def draw(self, surface):
        """
        draws the ship on a surface with an applied rotation
        """
        angle_to_transform = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle_to_transform, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * .5
        surface.blit(rotated_surface, blit_position)


class Asteroid(GameObject):
    """
    initializes an asteroid with random velocity from a given sprite
    """

    def __init__(self, position):
        super().__init__(position, load_sprite("ship"), get_random_velocity(1, 2))


class Bullet(GameObject):
    def __init__(self, position, velocity):
        """
        initializes a bullet from a given sprite
        """
        super().__init__(position, load_sprite("bullet"), velocity)

    def move(self, surface):
        """
        override GameObject.move() so bullets do not wrap the screen upon exit
        """
        self.position = self.position + self.velocity
