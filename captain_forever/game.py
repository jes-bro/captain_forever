import pygame
from utils import load_sprite, get_random_position
from models import GameObject, Ship, Asteroid


class CaptainForever:
    ENEMY_SPAWN_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space_background", 800, 600, False)
        self.clock = pygame.time.Clock()

        self.player_ship = Ship((400, 400))
        self.asteroids = []
        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.player_ship.position)
                    > self.ENEMY_SPAWN_DISTANCE
                ):
                    break
            self.asteroids.append(Asteroid(position))

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
        if is_key_pressed[pygame.K_UP]:
            self.player_ship.accelerate()

    def _get_game_objects(self):
        return [*self.asteroids, self.player_ship]

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(60)
