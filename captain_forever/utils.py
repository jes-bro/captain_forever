import random
from pygame import sprite
from pygame import Color
from pygame.image import load
from pygame.transform import scale
from pygame.math import Vector2
from pygame.mixer import Sound
import os
from pygame_animatedgif import AnimatedGifSprite


# stores horizontal and vertical dimensions of pngs that need to be scaled
dimensions = {"ship": (150, 200)}


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
    loaded_sprite.rect = loaded_sprite.image.get_rect()
    if name in dimensions and with_scaling == True:
        loaded_sprite = scale(
            loaded_sprite, (dimensions[name][0], dimensions[name][1]))
    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


# Blow up enemy ship
def explode(x_coord, y_coord):
    """
    Displays explosion sprite in place of enemy
    """
    explosion = AnimatedGifSprite(
        (x_coord, y_coord), "../assets/sprites/explosion.gif")
    sprite_group = sprite.Group()
    sprite_group.add(explosion)

    return sprite_group


def load_sound(name):
    """
    loads a sound from sound assets by its name
    """
    path = f"../assets/sounds/{name}.mp3"
    # return Sound(path)


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
        random.randrange(surface.get_width()), random.randrange(
            surface.get_height())
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


def print_text(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, True, color)

    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)
