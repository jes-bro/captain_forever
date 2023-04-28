import pygame
from utils import load_sprite
from models import GameObject, Ship


class CaptainForever:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space_background", 800, 600, False)
        self.clock = pygame.time.Clock()
        self.player_ship = Ship((400, 400))

        # ALL npc lines commented upon removal of Gameobject and implement of ship
        # self.npc = GameObject((10, 10), load_sprite("ship", 150, 200), (1, 0))

        # self.player_ship = pygame.transform.scale(self.player_ship, (35, 35))
        # self.npc = pygame.transform.scale(self.mpc, (35, 35))

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
        is_key_pressed = pygame.key.get_pressed()

        if is_key_pressed[pygame.K_RIGHT]:
            self.player_ship.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.player_ship.rotate(clockwise=False)

    def _process_game_logic(self):
        # self.npc.move()
        self.player_ship.move()

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player_ship.draw(self.screen)
        # self.npc.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)
