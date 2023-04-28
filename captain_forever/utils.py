from pygame.image import load
from pygame.transform import scale
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
    loaded_sprite = scale(loaded_sprite, (horizontal_dim, vertical_dim))
    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()
