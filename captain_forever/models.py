import pygame
from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import load_sprite

# Because pygame has inverted y axis, this vector points UP (used for calculations)
UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self):
        self.position = self.position + self.velocity

    def collides_with(self, other_obj):
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

    def __init__(self, position):
        """
        initializes Ship (NPC and player)
        """
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

    def draw(self, surface):
        """
        draws the ship on a surface with an applied rotation
        """
        angle_to_transform = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle_to_transform, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * .5
        surface.blit(rotated_surface, blit_position)
