# pylint: disable=no-member
# pylint: disable=no-name-in-module
# Disabling pylint warnings related to PyGame that aren't valid
"""
Main file that executes our game and initializes classes.
"""
import pygame
from game import CaptainForever
from controller import ArrowController
from view import PyGameView

if __name__ == "__main__":
    pygame.init()
    WIDTH = 1082
    HEIGHT = 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Captain Forever")
    captain_forever_game_instance = CaptainForever(WIDTH, HEIGHT)
    captain_forever_controller = ArrowController(
        captain_forever_game_instance, WIDTH, HEIGHT
    )
    captain_forever_view = PyGameView(captain_forever_game_instance, screen)
    captain_forever_game_instance.main_loop(
        captain_forever_controller, captain_forever_view
    )
