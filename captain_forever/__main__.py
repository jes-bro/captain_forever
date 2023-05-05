import pygame
from game import CaptainForever
from controller import ArrowController
from view import PyGameView

if __name__ == "__main__":
    pygame.init()
    width = 1082
    height = 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Captain Forever")
    captain_forever_game_instance = CaptainForever(width, height)
    captain_forever_controller = ArrowController(captain_forever_game_instance)
    captain_forever_view = PyGameView(captain_forever_game_instance, screen)
    captain_forever_game_instance.main_loop(
        captain_forever_controller, captain_forever_view
    )
