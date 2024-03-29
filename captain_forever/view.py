# pylint: disable=no-member
# pylint: disable=no-name-in-module
# Disabling pylint warnings related to PyGame that aren't valid
"""
Define Captain Forever view class.
"""
from abc import ABC, abstractmethod
import pygame
from pygame.math import Vector2
from pygame import Color
from utils import load_sprite


class CaptainForeverView(ABC):
    """
    Display the game.

    Attributes:
        _game: An instance of the captain forever
        game's state.
    """

    def __init__(self, game):
        """
        Initialize CaptainForeverView instance.

        Args:
            game: An instance of the game
            class to display.
        """
        self._game = game

    @property
    def game(self):
        """
        Return _game.

        Returns:
            _game: An instance of CaptainForever with
            current game state.
        """
        return self._game

    @abstractmethod
    def draw(self):
        """
        Display the game.
        """


class PyGameView(CaptainForeverView):
    """
    Display the game elements using Pygame.
    """

    def __init__(self, game, screen):
        """
        Initialize the PyGame Display.

        Attributes:
            _clock: PyGame clock instance, tracks game time.
            _screen: PyGame surface display instance, surface to draw game
            objects.
            _background: PyGame surface, background of game drawn each frame.
            _font: PyGame font instance, controls font of endgame message.
        """
        super().__init__(game)
        self._screen = screen
        self._background = load_sprite("background", False, True)
        self._clock = pygame.time.Clock()
        self._font = pygame.font.Font(None, 64)

    def draw(self):
        """
        draws the game objects onto the display
        """
        game = self.game
        game.counter += 1
        if game.counter % 50 == 0 and game.fires:
            game.fires.pop()
        self._screen.blit(self._background, (0, 0))
        for game_object in game.get_game_objects():
            game_object.draw(self._screen)

        if game.message:
            print_text(self._screen, game.message, self._font)

        pygame.display.flip()
        self._clock.tick(60)


def print_text(surface, text, font, color=Color("tomato")):
    """
    Blit text to the screen so that users know how
    to proceed in the game.

    Args:
        surface: An instance of a PyGame surface.
        text: A string representing the text to be
        displayed.
        font: PyGame font object, used to determine
        the font of the message.
        color: A PyGame color object, used to determine
        the color of the message.
    """
    if "\n" in text:
        lines = text.split("\n")
        line_surfaces = []
        # adding initial height so lines have a buffer
        total_height = 50
        for line in lines:
            text_surface = font.render(line, True, color)
            total_height += text_surface.get_height()
            line_surfaces.append(text_surface)
        # centering text on the screen
        total_height = total_height / 2
        for line_surface in line_surfaces:
            rect = line_surface.get_rect()
            rect.center = (Vector2(surface.get_size()) / 2) - Vector2(
                0, total_height
            )
            total_height -= line_surface.get_height()
            surface.blit(line_surface, rect)
    else:
        text_surface = font.render(text, True, color)

        rect = text_surface.get_rect()
        rect.center = Vector2(surface.get_size()) / 2

        surface.blit(text_surface, rect)
