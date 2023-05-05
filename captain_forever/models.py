import pygame
from pygame.math import Vector2
from pygame import Color
from pygame.transform import rotozoom
from utils import (
    get_random_velocity,
    load_sprite,
    wrap_position,
)  # , load_sound
from pygame.locals import *

# Because pygame has inverted y axis, this vector points UP (used for calculations)
UP = Vector2(0, -1)


class GameObject:
    """ "
    Game Object for storing sprites and attributes for game state and drawing

    Attributes:
        position: Vector2, x and y position on the screen
        sprite: Pygame surface, image with some width and height
        radius: int, radius of the sprite
        velocity: Vector2, rate of change in x and y of the sprite
        method_flag: Int, used to identify which function was called during testing.

    Methods:
        draw: draw object on a surface at position
        move: move object's position by velocity (does not move, velocity = 0)
        collides_with: calculate bool of whether object is colliding with another object
    """

    def __init__(self, position, sprite, velocity):
        """
        Initialize a GameObject instance.
        """
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        self.method_flag = 0

    def draw(self, surface):
        """
        Draw the game object onto a surface at its current position.

        Args:
            surface: pygame surface, surface on which object will be drawn
        """
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        """
        Move game objects and wrap surface-exiting objects back onto surface

        Args:
            surface: pygame surface, surface on which object will be drawn
        """
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        """
        Return whether a collision has occured between two game objects (bool)

        Args:
            other_obj: class instance inherited from GameObject with radius attribute
        """
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class StaticObject(GameObject):
    """
    creates an object that does not move

    Attributes:
        position: Vector2, x and y position on the screen
        sprite: Pygame surface, image with some width and height
        radius: int, radius of the sprite
        velocity: Vector2, (0, 0) because these objects do not move

    Methods:
        draw: draw object on a surface at position
        move: move object's position by velocity (does not move, velocity = 0)
        collides_with: calculate bool of whether object is colliding with another object
    """

    def __init__(self, position, name):
        """
        initializes static object
        """
        super().__init__(
            position, load_sprite(f"{name}", True, True), Vector2(0)
        )


class Ship(GameObject):
    """
    Class for player and npc ship instances

    Constants:
        MANEUVERABILITY: Int, degrees per second a ship can turn.
        ACCELERATION: Float, rate of cartesian transform velocity change.

    Attributes:
        position: Tuple of ints, position (x, y) on surface to draw the ship.
        create_bullet_callback: Function, function to add bullets to list to be processed.
        name: Str, name of the file which the ship png is located in.
        direction: Vector2, x and y vector that shows orientation of sprite.
        _health: Int, number of hits before the ship will die.


    Methods:
        rotate: Rotate the ship's direction by MANEUVERABILITY degrees.
        accelerate: Increase the ship velocity by ACCELERATION.
        deccelerate: Increase the ship velocity by ACCELERATION.
        shoot: create Bullet instance with speed BULLET_SPEED.
        draw: Draw the ship on a surface with an applied rotation.
        reduce_health: Reduces _health by 1.
        move: Move object's position by velocity (does not move, velocity = 0).
        collides_with: Calculate bool of whether object is colliding with another object.

    """

    MANEUVERABILITY = 3
    ACCELERATION = 0.20  # 0.25
    BULLET_SPEED = 9
    # LASER_SOUND = load_sound("laser")

    def __init__(
        self, position, create_bullet_callback, name, with_alpha, with_scaling
    ):
        """
        Initialize Ship (NPC and player) and bullet callbacks.
        """
        # creates callback for game to access bullets
        self.create_bullet_callback = create_bullet_callback
        self._health = 3

        # initialize unit vector upwards initial direction
        self.direction = Vector2(UP)
        super().__init__(
            position,
            load_sprite(f"{name}", with_alpha, with_scaling),
            Vector2(0),
        )

    def rotate(self, clockwise=True):
        """
        Rotate the direction vector of the ship by MANEUVERABILITY degrees.

        Args:
            clockwise: Bool, whether the rotation is in clockwise direction.
        """
        self.method_flag = 4
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self, acceleration_factor):
        """
        Increase velocity of the ship in the direction it is facing.

        Args:
            acceleration_factor: Float, amount the velocity is increased by.
        """
        self.method_flag = 5
        self.velocity += acceleration_factor * (
            self.direction * self.ACCELERATION
        )

    def deccelerate(self, deceleration_factor):
        """
        Decrease velocity of the ship in the direction it is facing.

        Args:
            deceleration_factor: Float, amount the velocity is decreased by.
        """
        self.method_flag = 6
        self.velocity -= deceleration_factor * (
            self.direction * self.ACCELERATION
        )

    def shoot(self):
        """
        Creates a bullet instance shooting in the direction of the ship from its position.
        """
        self.method_flag = 1
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)

    def draw(self, surface):
        """
        Draw the ship sprite on a surface with an applied rotation.

        Args:
            surface: PyGame surface, surface on which object will be drawn.
        """
        angle_to_transform = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle_to_transform, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def reduce_health(self):
        """
        Reduce the ship health attribute by 1.
        """
        self._health = self._health - 1

    def get_health(self):
        """
        Return the health of ship.
        """
        return self._health


class NPCShip(Ship):
    """
    Ship controlled by the computer.
    """

    BULLET_DELAY = 1

    def __init__(self, position, name, create_bullet_callback):
        self._position = position
        super().__init__(
            self._position, create_bullet_callback, name, True, True
        )
        self._health = 2
        self.clock = pygame.time.Clock()
        self._shooting_delay = 0

        # creating new surface to recolor sprite
        recolor_surface = pygame.Surface(
            self.sprite.get_size(), pygame.SRCALPHA
        )
        recolor_surface.fill(pygame.color.Color("green"))
        self.sprite.blit(
            recolor_surface, (0, 0), special_flags=pygame.BLEND_ADD
        )

    def move(self, surface, player):
        """
        Rotate the NPC ship to track player, approach upon appropriate heading

        Args:
            surface: PyGame surface, surface on which object will be drawn
            player: Ship instance, player ship with position attribute
        """
        # Find direction vector (dx, dy) between enemy and player.
        player_position = player.position
        dirvect = pygame.math.Vector2(
            player_position[0] - self.position[0],
            player_position[1] - self.position[1],
        )
        error_angle = self.direction.angle_to(dirvect)
        if error_angle > 3 or error_angle < -3:
            self.rotate(clockwise=(error_angle > 0))
        else:
            self.velocity = Vector2(0)
            self.shoot()
            self.method_flag = 8
            if dirvect.magnitude() > 300:
                self.velocity = dirvect.normalize() * 2
            if dirvect.magnitude() < 150:
                self.velocity = dirvect.normalize() * -2

        # Move along this normalized vector towards the player at current speed.
        self.position = wrap_position(self.position + self.velocity, surface)

    def shoot(self):
        """
        Creates a bullet shooting in the direction of the ship from its position.
        """
        self._shooting_delay += 9
        if self._shooting_delay > 1000 * self.BULLET_DELAY:
            self._shooting_delay = 0
            bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
            bullet = Bullet(self.position, bullet_velocity)
            self.create_bullet_callback(bullet)


class Bullet(GameObject):
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
        override GameObject.move() so bullets do not wrap the screen upon exit.
        """
        self.position = self.position + self.velocity
