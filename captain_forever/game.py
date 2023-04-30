import pygame
from utils import load_sprite, load_sound, get_random_position, print_text, explode
from models import GameObject, Ship, NPCShip


class CaptainForever:
    ENEMY_SPAWN_DISTANCE = 400

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space_background", False, True)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.npc_ships = []
        self.bullets = []
        self.player_ship = Ship(
            (400, 400), self.bullets.append, "player", True, False)

        for _ in range(2):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.player_ship.position)
                    > self.ENEMY_SPAWN_DISTANCE
                ):
                    break
            self.npc_ships.append(NPCShip(position))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Captain Forever")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                self.player_ship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.player_ship.shoot()
        is_key_pressed = pygame.key.get_pressed()

        if self.player_ship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.player_ship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.player_ship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.player_ship.accelerate()
            elif is_key_pressed[pygame.K_DOWN]:
                self.player_ship.deccelerate()

    def _get_game_objects(self):
        """
        returns all game objects that have not been destroyed
        """
        game_objects = [*self.npc_ships, *self.bullets]

        if self.player_ship:
            game_objects.append(self.player_ship)
        return game_objects

    def _process_game_logic(self):
        """
        processes movement on non-destroyed game objects
        """
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
        if self.player_ship:
            for npc_ship in self.npc_ships:
                if npc_ship.collides_with(self.player_ship):
                    self.player_ship = None
                    self.message = "You lost!"
                    break
        # Check for bullet not hitting anything
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)
        # Check for bullet collisions with npc ships
        for bullet in self.bullets[:]:
            for npc_ship in self.npc_ships[:]:
                if npc_ship.collides_with(bullet):
                    position_on_screen = npc_ship.get_position()
                    sprite_group = explode(
                        position_on_screen[0], position_on_screen[1])
                    sprite_group.update(self.screen)
                    sprite_group.draw(self.screen)
                    self.npc_ships.remove(npc_ship)

                    self.bullets.remove(bullet)
                    npc_ship.split()
                    # load_sound("rock").play()

                    break
        if not self.npc_ships and self.player_ship:
            self.message = "You won!"

    def _draw(self):
        """
        draws the game objects onto the display
        """
        self.screen.blit(self.background, (0, 0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(60)
