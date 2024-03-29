# pylint: disable=no-member
# pylint: disable=no-name-in-module
# Disabling pylint warnings related to PyGame that aren't valid
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
        _width: Int, representing width of the screen.
        _height: Int, representing height of the screen.
    """

    # Define your methods here.
    def __init__(self, game, width, height):
        """
        Initialize CaptainForeverController.

        Args:
            game: An instance of the captain forever class
            that gives the state of the game.
            width: Int, representing width of the screen.
            height: Int, representing height of the screen.
        """
        self._game = game
        self._width = width
        self._height = height

    @property
    def game(self):
        """
        Return _game.

        Returns: _game, the state of the game.
        """
        return self._game

    @abstractmethod
    def maneuver_player_ship(self):
        """
        Move the player ship based on user input.
        """


class ArrowController(CaptainForeverController):
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
                and game_state.is_running
            ):
                game_state.player_ship.shoot()

            elif event.type == pygame.KEYDOWN and (
                event.key == pygame.K_KP_ENTER
                or event.key == pygame.K_RETURN
                and not game_state.is_running
            ):
                game_state.__init__(self._width, self._height)

        if game_state.is_running:
            is_key_pressed = pygame.key.get_pressed()
            if is_key_pressed[pygame.K_RIGHT]:
                game_state.player_ship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                game_state.player_ship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                game_state.player_ship.accelerate(acceleration_factor=0.5)
            elif is_key_pressed[pygame.K_DOWN]:
                game_state.player_ship.deccelerate(deceleration_factor=0.5)
