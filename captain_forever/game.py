import pygame
from utils import load_sprite
from models import GameObject


class CaptainForever:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space_background", 800, 600, False)
        self.player_ship = GameObject(
            (10, 10), load_sprite("player_ship", 150, 150), (0, 0)
        )
        self.mpc = GameObject((10, 10), load_sprite("ship", 150, 200), (1, 0))
        # self.player_ship = pygame.transform.scale(self.player_ship, (35, 35))
        # self.mpc = pygame.transform.scale(self.mpc, (35, 35))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()

    def _process_game_logic(self):
        self.mpc.move()
        self.player_ship.move()

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player_ship.draw(self.screen)
        self.mpc.draw(self.screen)
        pygame.display.flip()
