import pygame
from pygame.math import Vector2
from pygame import Color
from pygame.transform import rotozoom
from utils import get_random_velocity, load_sound, load_sprite, wrap_position
from pygame.locals import *

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


class StaticObject(GameObject):
    """
    creates an object that does not move
    """

    def __init__(self, position, name):
        """
        initializes static object
        """
        super().__init__(position, load_sprite(
            f"{name}", True, True), Vector2(0))


class Ship(GameObject):
    """
    represents player and npc ship instances

    Constants:
        MANEUVERABILITY: int, degrees per second a ship can turn
        ACCELERATION: float, rate of cartesian transform velocity change

    Args:
        position: tuple of ints, position (x, y) on surface to draw the ship

    Methods:
        rotate: rotates the ship by MANEUVERABILITY degrees
        draws the ship on a surface with an applied rotation

    """

    MANEUVERABILITY = 3
    ACCELERATION = 0.20  # 0.25
    BULLET_SPEED = 9
    LASER_SOUND = load_sound("laser")

    def __init__(self, position, create_bullet_callback, name, with_alpha, with_scaling):
        """
        initializes Ship (NPC and player) and bullet callbacks
        """
        # creates callback for game to access bullets
        self.create_bullet_callback = create_bullet_callback
        self._health = 3

        # initialize unit vector upwards initial direction
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite(
            f"{name}", with_alpha, with_scaling), Vector2(0))

    def rotate(self, clockwise=True):
        """
        rotate the direction vector of the ship by MANEUVERABILITY degrees
        """
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self, acceleration_factor):
        """
        increases velocity of the ship in the direction it is facing
        """
        self.velocity += acceleration_factor * \
            (self.direction * self.ACCELERATION)

    def deccelerate(self, deceleration_factor):
        """
        decreases velocity of the ship in the direction it is facing
        """
        self.velocity -= deceleration_factor * \
            (self.direction * self.ACCELERATION)

    def shoot(self):
        """
        creates a bullet shooting in the direction of the ship from its position
        """
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        # self.laser_sound.play()

    def draw(self, surface):
        """
        draws the ship on a surface with an applied rotation
        """
        angle_to_transform = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle_to_transform, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def reduce_health(self):
        """
        Reduces the ship health attribute by 1
        """
        self._health = self._health - 1

# TODO: get rid of this cause position is not private
    def get_position(self):
        """
        Return the x, y coord of npc or player on the screen.
        """
        return self.position

    def get_health(self):
        """
        Return the health of ship.
        """
        return self._health


class NPCShip(Ship):
    """
    Ship controlled by the computer
    """

    BULLET_DELAY = 1

    def __init__(self, position, name, create_bullet_callback):
        self._position = position
        super().__init__(self._position, create_bullet_callback, name, True, True)
        self._health = 2
        self.clock = pygame.time.Clock()
        self._shooting_delay = 0

        # creating new surface to recolor sprite
        recolor_surface = pygame.Surface(
            self.sprite.get_size(), pygame.SRCALPHA)
        recolor_surface.fill(pygame.color.Color("green"))
        self.sprite.blit(recolor_surface, (0, 0),
                         special_flags=pygame.BLEND_ADD)

    def move(self, surface, player):
        # Find direction vector (dx, dy) between enemy and player.
        player_position = player.get_position()
        dirvect = pygame.math.Vector2(
            player_position[0] -
            self.position[0], player_position[1] - self.position[1]
        )
        error_angle = self.direction.angle_to(dirvect)
        if error_angle > 3 or error_angle < -3:
            self.rotate(clockwise=(error_angle > 0))
        else:
            self.velocity = Vector2(0)
            self.shoot()
            if dirvect.magnitude() > 300:
                self.velocity = dirvect.normalize() * 2
            if dirvect.magnitude() < 150:
                self.velocity = dirvect.normalize() * -2

        # Move along this normalized vector towards the player at current speed.
        self.position = wrap_position(self.position + self.velocity, surface)

    def shoot(self):
        """
        creates a bullet shooting in the direction of the ship from its position
        """
        self._shooting_delay += 9
        if self._shooting_delay > 1000*self.BULLET_DELAY:
            self._shooting_delay = 0
            bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
            bullet = Bullet(self.position, bullet_velocity)
            self.create_bullet_callback(bullet)


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
