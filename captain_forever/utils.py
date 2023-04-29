import random
from pygame.image import load
from pygame.transform import scale
from pygame.math import Vector2
import os


def load_sprite(name, horizontal_dim=150, vertical_dim=200, with_alpha=True):
    """
    loads a sprite from assets/sprites to a surface with or without alpha

    inputs: 
        horizontal_dim: int, pix width
        verical_dim: int, pix height
        with_alpha: bool, whether to convert image for faster processing
    """
    # os.chdir("C:/Users/jbrown/Desktop/captain_forever/Captain_Forever_Project")
    loaded_sprite = load(f"../assets/sprites/{name}.png")
    # loaded_sprite = scale(loaded_sprite, (horizontal_dim, vertical_dim))
    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def wrap_position(position, surface):
    """
    re-maps coordinates off of a surface's size back to real points

    inputs:
        position: tuple of ints, position on the surface (0, 0 is top left)
        surface: pygame surface, typically the display surface
    """
    (x, y) = position
    (w, h) = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_position(surface):
    """
    returns a random position within a surface

    inputs: 
        surface: pygame surface, coordinates will be within maximum bounds

    returns: 
        random_position: Vector2 2 item position vector, random pos
    """
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height())
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
