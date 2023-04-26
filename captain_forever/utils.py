from pygame.image import load
import os

def load_sprite(name, with_alpha=True):
    os.chdir("../")
    loaded_sprite = load(f"assets\sprites\{name}.png")

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()