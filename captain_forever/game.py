import pygame
from utils import load_sprite, get_random_position
from models import Ship, NPCShip, StaticObject


class CaptainForever:
    ENEMY_SPAWN_DISTANCE = 400

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space_background", False, True)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""
        self.counter = 0
        self.fires = []
        self.npc_ships = []
        self.npc_bullets = []
        self.bullets = []
        self.player_ship = Ship(
            (400, 400), self.bullets.append, "player", True, False)
        self.enemy_spawn_counter = 0
        for _ in range(3):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.player_ship.position)
                    > self.ENEMY_SPAWN_DISTANCE
                ):
                    break
            # second argument specifies ship and not fire
            self.npc_ships.append(
                NPCShip(position, "ship", self.npc_bullets.append))

    def main_loop(self, controller, view):
        while True:
            controller.maneuver_player_ship()
            self._process_game_logic()
            view.draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Captain Forever")

    def _get_game_objects(self):
        """
        returns all game objects that have not been destroyed
        """
        game_objects = [*self.npc_ships, *self.bullets,
                        *self.npc_bullets, *self.fires]

        if self.player_ship:
            game_objects.append(self.player_ship)
        return game_objects

    def _process_game_logic(self):
        """
        processes movement on non-destroyed game objects
        """
        if not self.message:
            for game_object in self._get_game_objects():
                if game_object in self.npc_ships:  # or game_object in self.fires:
                    game_object.move(self.screen, self.player_ship)
                else:
                    game_object.move(self.screen)
            for npc_ship in self.npc_ships:
                if npc_ship.collides_with(self.player_ship):
                    self.player_ship = StaticObject(
                        self.player_ship.position, "fire")
                    self._end_game_message("lost")
                    # What would be nice is if it paused for a sec and returned to a start menu
                    break
            if len(self.npc_ships) < 8:
                self.enemy_spawn_counter += 5
                # enemy spawning scales with number of enemies left
                if self.enemy_spawn_counter > len(self.npc_ships)*125:
                    self.enemy_spawn_counter = 0
                    self._spawn_enemy()

        # Check for bullet not hitting anything
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        for bullet in self.npc_bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.npc_bullets.remove(bullet)

        # Check for bullet collisions with npc ships
        for bullet in self.bullets[:]:
            for npc_ship in self.npc_ships[:]:
                if npc_ship.collides_with(bullet):
                    position_on_screen = npc_ship.get_position()
                    self.npc_ships.remove(npc_ship)
                    fire = StaticObject(position_on_screen, "fire")
                    self.fires.append(fire)

        for bullet in self.npc_bullets[:]:
            if self.player_ship.collides_with(bullet):
                self.npc_bullets.remove(bullet)
                self.player_ship.reduce_health()
                if self.player_ship.get_health() == 0:
                    self.player_ship = StaticObject(
                        self.player_ship.position, "fire")
                    self._end_game_message("lost")

        if not self.npc_ships and self.player_ship:
            self._end_game_message("won")

    def _end_game_message(self, won_lost_str):
        """
        displays a won/lost string at the end of the game
        """
        self.message = f"You {won_lost_str}! \n To exit, press escape \n To start a new game, press enter"

    def _spawn_enemy(self):
        """
        Spawn in new enememy ship.
        """
        while True:
            position = get_random_position(self.screen)
            if (
                position.distance_to(self.player_ship.position)
                < self.ENEMY_SPAWN_DISTANCE
            ):
                break
            # second argument specifies ship and not fire
            self.npc_ships.append(
                NPCShip(position, "ship", self.npc_bullets.append))
