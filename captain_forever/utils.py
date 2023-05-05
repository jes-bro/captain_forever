# pylint: disable=no-member
# pylint: disable=no-name-in-module
# Disabling pylint warnings related to PyGame that aren't valid
"""
Utility functions that support gameplay.
"""
import random
from pygame.image import load
from pygame.transform import scale
from pygame.math import Vector2


# stores horizontal and vertical dimensions of pngs that need to be scaled
dimensions = {
    "ship": (50, 50),
    "space_background": (1000, 800),
    "fire": (100, 100),
    "background": (1082, 720),
}


def load_sprite(name, with_alpha=True, with_scaling=False):
    """
    loads a sprite from assets/sprites to a surface with or without alpha

    inputs:
        horizontal_dim: int, pix width
        verical_dim: int, pix height
        with_alpha: bool, whether to convert image for faster processing
    """
    # os.chdir("C:/Users/jbrown/Desktop/captain_forever/Captain_Forever_Project")
    loaded_sprite = load(f"../assets/sprites/{name}.png")
    if name in dimensions and with_scaling is True:
        loaded_sprite = scale(
            loaded_sprite, (dimensions[name][0], dimensions[name][1])
        )
    if with_alpha:
        return loaded_sprite.convert_alpha()
    return loaded_sprite.convert()


# def load_sound(name):
#     """
#     loads a sound from sound assets by its name
#     """
#     path = f"../assets/sounds/{name}.mp3"
#     # return Sound(path)


def wrap_position(position, width, height):
    """
    re-maps coordinates off of a surface's size back to real points

    inputs:
        position: tuple of ints, position on the surface (0, 0 is top left)
        surface: pygame surface, typically the display surface
        width: Int, represents width of screen.
        height: Int, represents height of screen.
    """
    (x_coordinate, y_coordinate) = position
    return Vector2(x_coordinate % width, y_coordinate % height)


def get_random_position(width, height):
    """
    returns a random position within a surface

    inputs:
        surface: pygame surface, coordinates will be within maximum bounds

    returns:
        random_position: Vector2 2 item position vector, random pos
    """
    return Vector2(
        random.randrange(width),
        random.randrange(height),
    )


def get_random_velocity(min_speed, max_speed):
    """
    generates a randomly oriented vector with magnitude between min and max speed

    inputs:
        min_speed: int, min speed (magnitude of velocity) in pix/second
        max_speed: int, max speed (magnitude of velocity) in pix/second
    """
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)
