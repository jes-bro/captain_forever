# pylint: disable=no-member
# pylint: disable=no-name-in-module
# Disabling pylint warnings related to PyGame that aren't valid
"""
Define the classes corresponding to our model architecture and update
their properties to reflect game state.
"""
import pygame
from pygame.math import Vector2
from pygame.transform import rotozoom
from pygame.locals import *
from utils import (
    load_sprite,
    wrap_position,
)

# Because pygame has inverted y axis, this vector points UP (used for calculations)
UP = Vector2(0, -1)


class GameObject:
    """
    Game Object for storing sprites and attributes for game state and drawing.

    Attributes:
        _position: Vector2, x and y position on the screen.
        _sprite: Pygame surface, image with some width and height.
        _radius: int, radius of the sprite.
        _velocity: Vector2, rate of change in x and y of the sprite.
        _method_flag: Int, used to identify which function was called during testing.
    """

    def __init__(self, position, sprite, velocity):
        """
        Initialize a GameObject instance.
        """
        self._position = Vector2(position)
        self._sprite = sprite
        self._radius = sprite.get_width() / 2
        self._velocity = Vector2(velocity)
        self._method_flag = 0

    @property
    def position(self):
        """
        Return _position.

        Returns:
            _position: Vector2, representing x,y object pos on screen.
        """
        return self._position

    @property
    def sprite(self):
        """
        Return _sprite.

        Returns:
            _sprite: PyGame Sprite representing model object.
        """
        return self._sprite

    @property
    def radius(self):
        """
        Return _radius.

        Returns:
            _radius: Int, representing radius of sprite.
        """
        return self._radius

    @property
    def velocity(self):
        """
        Return _velocity.

        Returns:
            _velocity: Vector2, representing magnitude and
            direction of velocity of object.
        """
        return self._velocity

    @property
    def method_flag(self):
        """
        Return _method_flag.

        Returns:
            _method_flag: Int, helps determine whether function.
            has been called for unit testing.
        """
        return self._method_flag

    def draw(self, surface):
        """
        Draw the game object onto a surface at its current position.

        Args:
            surface: PyGame surface on which the sprite will be drawn.
        """
        blit_position = self._position - Vector2(self._radius)
        surface.blit(self._sprite, blit_position)

    def move(self, width, height):
        """
        Move game objects and wrap surface-exiting objects back onto surface.

        Args:
            surface: pygame surface, surface on which object will be drawn.
            width: Int, represents width of screen.
            height: Int, represents height of screen.
        """
        self._position = wrap_position(
            self._position + self._velocity, width, height
        )

    def collides_with(self, other_obj):
        """
        Return whether a collision has occured between two game objects (bool)

        Args:
            other_obj: class instance inherited from GameObject with radius attribute

        Returns:
            Bool representing whether the objects are colliding or not.
        """
        distance = self._position.distance_to(other_obj.position)
        return distance < self._radius + other_obj.radius


class StaticObject(GameObject):
    """
    Create an object that does not move.


    Attributes:
        _position: Vector2, x and y position on the screen.
        _sprite: Pygame surface, image with some width and height.
        _radius: int, radius of the sprite.
        _velocity: Vector2, rate of change in x and y of the sprite.
        _method_flag: Int, used to identify which function was called during testing.
    """

    def __init__(self, position, name):
        """
        Initializes static object.

        Args:
            position: Vector2, x and y position on the screen
            name: Str, name of the file which the ship png is located in.
        """
        super().__init__(
            position, load_sprite(f"{name}", True, True), Vector2(0)
        )


class Ship(GameObject):
    """
    Class for player and NPCShip instances.

    Constants:
        MANEUVERABILITY: Int, degrees per second a ship can turn.
        ACCELERATION: Float, rate of cartesian transform velocity change.
        BULLET_SPEED: Int, representing speed of bullet.

    Attributes:
        _direction: Vector2, x and y vector that shows orientation of sprite.
        _health: Int, number of hits before the ship will die.
        _create_bullet_callback: Function, function to add bullets to list to be processed.
        _position: Vector2, x and y position on the screen
        _sprite: Pygame surface, image with some width and height
        _radius: int, radius of the sprite
        _velocity: Vector2, rate of change in x and y of the sprite
        _method_flag: Int, used to identify which function was called during testing.
    """

    MANEUVERABILITY = 3
    ACCELERATION = 0.20
    BULLET_SPEED = 9

    def __init__(
        self, position, create_bullet_callback, name, with_alpha, with_scaling
    ):
        """
        Initialize Ship (NPC and player) and bullet callbacks.

        Args:
            name: Str, name of the file which the ship png is located in.
            position: Vector2, x and y position on the screen
            create_bullet_callback: Function, function to add bullets to list to be processed.
            with_alpha: Bool, representing whether sprite should be loaded as transparent.
            with_scaling: Bool, representing whether sprite should be scaled or not.
        """
        # creates callback for game to access bullets
        self._create_bullet_callback = create_bullet_callback
        self._health = 3

        # initialize unit vector upwards initial direction
        self._direction = Vector2(UP)
        super().__init__(
            position,
            load_sprite(f"{name}", with_alpha, with_scaling),
            Vector2(0),
        )

    @property
    def direction(self):
        """
        Return _direction.

        Returns:
            _direction: Vector2, representing direction of object.
        """
        return self._direction

    def rotate(self, clockwise=True):
        """
        Rotate the direction vector of the ship by MANEUVERABILITY degrees.

        Args:
            clockwise: Bool, whether the rotation is in clockwise direction.
        """
        self._method_flag = 4
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self._direction.rotate_ip(angle)

    def accelerate(self, acceleration_factor):
        """
        Increase velocity of the ship in the direction it is facing.

        Args:
            acceleration_factor: Float, amount the velocity is increased by.
        """
        self._method_flag = 5
        self._velocity += acceleration_factor * (
            self._direction * self.ACCELERATION
        )

    def deccelerate(self, deceleration_factor):
        """
        Decrease velocity of the ship in the direction it is facing.

        Args:
            deceleration_factor: Float, amount the velocity is decreased by.
        """
        self._method_flag = 6
        self._velocity -= deceleration_factor * (
            self._direction * self.ACCELERATION
        )

    def shoot(self):
        """
        Creates a bullet instance shooting in the direction of the ship from its position.
        """
        self._method_flag = 1
        bullet_velocity = self._direction * self.BULLET_SPEED + self._velocity
        bullet = Bullet(self._position, bullet_velocity)
        self._create_bullet_callback(bullet)

    def draw(self, surface):
        """
        Draw the ship sprite on a surface with an applied rotation.

        Args:
            surface: PyGame surface, surface on which object will be drawn.
        """
        angle_to_transform = self._direction.angle_to(UP)
        rotated_surface = rotozoom(self._sprite, angle_to_transform, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self._position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def reduce_health(self):
        """
        Reduce the ship health attribute by 1.
        """
        self._health = self._health - 1

    def get_health(self):
        """
        Return the health of ship.

        Returns: _health, int representing health of ship.
        """
        return self._health


class NPCShip(Ship):
    """
    Define ship controlled by the computer.
    """

    BULLET_DELAY = 1

    def __init__(self, position, name, create_bullet_callback):
        """
        Initialize NPC ship.

        Args:
            position: Vector2, x and y position on the screen.
            name: String, name of png corresponding to object.
            create_bullet_callback: Function, function to add bullets
            to list to be processed.

        Attributes:
            _shooting_delay: Int, represents amt of time to wait before shotting
            player.
            _direction: Vector2, x and y vector that shows orientation of sprite.
            _health: Int, number of hits before the ship will die.
            _create_bullet_callback: Function, function to add bullets to list to be processed.
            _position: Vector2, x and y position on the screen.
            _sprite: Pygame surface, image with some width and height.
            _radius: int, radius of the sprite.
            _velocity: Vector2, rate of change in x and y of the sprite.
            _method_flag: Int, used to identify which function was called during testing.
        """
        self._position = position
        super().__init__(
            self._position, create_bullet_callback, name, True, True
        )
        self._health = 2
        self._shooting_delay = 0

        # creating new surface to recolor sprite
        recolor_surface = pygame.Surface(
            self._sprite.get_size(), pygame.SRCALPHA
        )
        recolor_surface.fill(pygame.color.Color("green"))
        self._sprite.blit(
            recolor_surface, (0, 0), special_flags=pygame.BLEND_ADD
        )

    def move(self, player, width, height):
        """
        Rotate the NPC ship to track player, approach upon appropriate heading

        Args:
            player: Ship instance, player ship with position attribute
            width: Int, represents width of screen.
            height: Int, represents height of screen.
        """
        # Find direction vector (dx, dy) between enemy and player.
        player_position = player.position
        dirvect = pygame.math.Vector2(
            player_position[0] - self._position[0],
            player_position[1] - self._position[1],
        )
        error_angle = self._direction.angle_to(dirvect)
        if error_angle > 3 or error_angle < -3:
            self.rotate(clockwise=error_angle > 0)
        else:
            self._velocity = Vector2(0)
            self.shoot()
            self._method_flag = 8
            if dirvect.magnitude() > 300:
                self._velocity = dirvect.normalize() * 2
            if dirvect.magnitude() < 150:
                self._velocity = dirvect.normalize() * -2

        # Move along this normalized vector towards the player at current speed.
        self._position = wrap_position(
            self._position + self._velocity, width, height
        )

    def shoot(self):
        """
        Create a bullet shooting in the direction of the ship from its position.
        """
        self._shooting_delay += 9
        if self._shooting_delay > 1000 * self.BULLET_DELAY:
            self._shooting_delay = 0
            bullet_velocity = (
                self._direction * self.BULLET_SPEED + self._velocity
            )
            bullet = Bullet(self._position, bullet_velocity)
            self._create_bullet_callback(bullet)


class Bullet(GameObject):
    """
    Define bullet object.

    Attributes:
        _position: Vector2, x and y position on the screen
        _sprite: Pygame surface, image with some width and height
        _radius: int, radius of the sprite
        _velocity: Vector2, rate of change in x and y of the sprite
        _method_flag: Int, used to identify which function was called during testing.
    """

    def __init__(self, position, velocity):
        """
        Initialize bullet from a given sprite.

        Args:
            position: Vector2 tuple of x and y initial position.
            velocity: Vector2 tuple of x and y velocity.
        """
        super().__init__(position, load_sprite("bullet"), velocity)

    def move(self):
        """
        Override GameObject.move() so bullets do not wrap the screen upon exit.
        """
        self._position = self._position + self._velocity
