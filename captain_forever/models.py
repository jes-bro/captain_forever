import pygame
from pygame.math import Vector2
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
    ACCELERATION = 0.20  # 0.25
    BULLET_SPEED = 3
    LASER_SOUND = load_sound("laser")

    def __init__(self, position, create_bullet_callback):
        """
        initializes Ship (NPC and player) and bullet callbacks
        """
        # creates callback for game to access bullets
        self.create_bullet_callback = create_bullet_callback
        self._health = 10

        # initialize unit vector upwards initial direction
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("ship"), Vector2(0))

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
        self.velocity += 0.5 * (self.direction * self.ACCELERATION)

    def deccelerate(self):
        """
        decreases velocity of the ship in the direction it is facing
        """
        self.velocity -= 0.5 * (self.direction * self.ACCELERATION)

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


class NPCShip(Ship):
    """
    Ship controlled by the computer
    """

    def __init__(self, position):
        self._position = position
        super().__init__(self._position, load_sprite("ship"), Vector2(0))

    def move_towards_player(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(
            player.rect.x - self.rect.x, player.rect.y - self.rect.y
        )
        dirvect.normalize()
        # Move along this normalized vector towards the player at current speed.
        dirvect.scale_to_length(self.speed)
        self.rect.move_ip(dirvect)

    def move_randomly():
        pass


class Asteroid(GameObject):
    """
    initializes an asteroid with random velocity from a given sprite

    attributes:
        size: int (1 to 3) that represents sprite size family of the asteroid
    """

    def __init__(self, position, create_asteroid_callback, size=3):
        """
        initializes an asteroid and its callback.
        Size 3 asteroids are fresh, any lower spawned from destruction of asteroid
        """
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {
            3: 1,
            2: 0.5,
            1: 0.25,
        }
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)

        super().__init__(position, sprite, get_random_velocity(1, 2))

    def split(self):
        """
        splits an asteroid into 2 smaller asteroids
        """
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)


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
