from pygame.image import load
from pygame.transform import scale
import os


def load_sprite(name, horizontal_dim, vertical_dim, with_alpha=True):
    os.chdir("C:/Users/jbrown/Desktop/captain_forever/Captain_Forever_Project")
    loaded_sprite = load(f"assets\sprites\{name}.png")
    loaded_sprite = scale(loaded_sprite, (horizontal_dim, vertical_dim))
    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()
