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
    Load a sprite onto the PyGame surface.

    Args:
        name: String, representing name of png to load.
        with_alpha: Bool, whether to make image transparent.
        with_scaling: Bool, represents whether image should be scald.
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


def wrap_position(position, width, height):
    """
    Re-map coordinates off of a surface's size back to real points.

    Args:
        position: Tuple of ints, position on the surface (0, 0 is top left)
        width: Int, represents width of screen.
        height: Int, represents height of screen.
    """
    (x_coordinate, y_coordinate) = position
    return Vector2(x_coordinate % width, y_coordinate % height)


def get_random_position(width, height):
    """
    Returns a vector pointing in a random direction.

    Args:
        width: Int, represents width of screen.
        height: Int, represents height of screen.

    Returns:
        Vector2 2 item position vector, at a random position.
    """
    return Vector2(
        random.randrange(width),
        random.randrange(height),
    )


def get_random_velocity(min_speed, max_speed):
    """
    Generates a randomly oriented vector with magnitude between min and max speed.

    Args:
        min_speed: Int, min speed (magnitude of velocity) in pix/second.
        max_speed: Int, max speed (magnitude of velocity) in pix/second.
    """
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)
