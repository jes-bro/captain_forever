"""
Captain Forever controller.
"""
from abc import ABC, abstractmethod
import pygame


class CaptainForeverController(ABC):
    """
    Define class that handles how users interact with the
    Captain Forever game.

    Attributes:
        _game: An instance of the Captain Forever game
        class.
    """

    # Define your methods here.
    def __init__(self, game):
        """
        Initialize CaptainForeverController.

        Args:
            game: An instance of the captain forever class
            that gives the state of the game.
        """
        self._game = game

    @property
    def game(self):
        """
        Return the state of the internal board
        _game attribute.
        """
        return self._game

    @abstractmethod
    def maneuver_player_ship(self):
        """
        Move the player ship based on user input.
        """


class WASDController(CaptainForeverController):
    """
    Define controller that takes WASD keys as
    user input.
    """

    def maneuver_player_ship(self):
        """
        Move the player ship based on user input.
        """
        game_state = self.game
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                game_state.player_ship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                game_state.player_ship.shoot()
        is_key_pressed = pygame.key.get_pressed()

        if not game_state.message:
            if is_key_pressed[pygame.K_RIGHT]:
                game_state.player_ship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                game_state.player_ship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                game_state.player_ship.accelerate(acceleration_factor=0.5)
            elif is_key_pressed[pygame.K_DOWN]:
                game_state.player_ship.deccelerate(deceleration_factor=0.5)

        if game_state.message:
            if is_key_pressed[pygame.K_KP_ENTER] or is_key_pressed[pygame.K_RETURN]:
                game_state.__init__()
