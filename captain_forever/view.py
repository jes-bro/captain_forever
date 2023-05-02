"""
Tic-tac-toe game view.
"""
import pygame
from abc import ABC, abstractmethod
from pygame.math import Vector2
from pygame import Color


class CaptainForeverView(ABC):
    """
    Display the board.

    Attributes:
        _game: An instance of the captain forever
        game's state.
    """

    # Define your methods here.
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
        Return the state of the internal board (TicTacToeBoard)
        attribute.
        """
        return self._game

    @abstractmethod
    def draw(self):
        """
        Display the board.
        """


class PyGameView(CaptainForeverView):
    """
    Display the game elements using Pygame.
    """

    def draw(self):
        """
        draws the game objects onto the display
        """
        game = self.game
        game.counter += 1
        if game.counter % 50 == 0 and game.fires:
            game.fires.pop()
        game.screen.blit(game.background, (0, 0))
        for game_object in game._get_game_objects():
            game_object.draw(game.screen)

        if game.message:
            print_text(game.screen, game.message, game.font)

        pygame.display.flip()
        game.clock.tick(60)


def print_text(surface, text, font, color=Color("tomato")):
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
        total_height = total_height/2
        for line_surface in line_surfaces:
            rect = line_surface.get_rect()
            rect.center = (Vector2(surface.get_size()) / 2) - \
                Vector2(0, total_height)
            total_height -= line_surface.get_height()
            surface.blit(line_surface, rect)
    else:
        text_surface = font.render(text, True, color)

        rect = text_surface.get_rect()
        rect.center = Vector2(surface.get_size()) / 2

        surface.blit(text_surface, rect)
