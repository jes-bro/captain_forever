# pylint: disable=no-member
# pylint: disable=no-name-in-module
# pylint: disable=protected-access
# Disabling pylint warnings related to PyGame that aren't valid
# Disabling protected access because we need to modify private vars to test
# certain conditions
"""
Test util functions to ensure they have the correct behavior.
"""
import unittest
from unittest.mock import MagicMock
import pygame
from utils import (
    load_sprite,
    wrap_position,
    get_random_position,
    get_random_velocity,
)
from view import print_text


class TestMyModule(unittest.TestCase):
    """
    Class for testing the utils functions.
    """

    def setUp(self):
        """
        Initialize TestMyModule class.

        Attributes:
            _screen: An instance of the PyGame screen
            class used to represent the screen in
            Captain Forever.
            _font: PyGame font object, used to determine
            the font of the message.
            _width: Int, represents width of screen.
            _height: Int, represents height of screen.
        """
        pygame.init()
        self._screen = pygame.display.set_mode((1082, 720))
        self._font = pygame.font.Font(None, 64)
        self._width = 1082
        self._height = 720

    def test_load_sprite(self):
        """
        Test loading a sprite under several conditions.
        """
        # Test loading a sprite with alpha and without scaling
        sprite = load_sprite("ship", with_alpha=True, with_scaling=False)
        self.assertIsNotNone(sprite)

        # Test loading a sprite without alpha and with scaling
        sprite = load_sprite(
            "space_background", with_alpha=False, with_scaling=True
        )
        self.assertIsNotNone(sprite)

    def test_wrap_position(self):
        """
        Test that position wrapping works as expected.
        """
        # Test wrapping position that is off the top of the screen
        position = (-50, -50)
        self._width = 800
        self._height = 600
        wrapped_position = wrap_position(position, self._width, self._height)
        self.assertEqual(wrapped_position, (750, 550))

        # Test wrapping position that is off the right of the screen
        position = (850, 300)
        wrapped_position = wrap_position(position, self._width, self._height)
        self.assertEqual(wrapped_position, (50, 300))

        # Test wrapping position that is off the bottom of the screen
        position = (400, 650)
        wrapped_position = wrap_position(position, self._width, self._height)
        self.assertEqual(wrapped_position, (400, 50))

        # Test wrapping position that is off the left of the screen
        position = (-50, 300)
        self._width = 800
        self._height = 600
        wrapped_position = wrap_position(position, self._width, self._height)
        self.assertEqual(wrapped_position, (750, 300))

    def test_get_random_position(self):
        """
        Test that get_random_position works as intended.
        """
        self._width = 800
        self._height = 600

        # Test getting a random position
        random_position = get_random_position(self._width, self._height)
        self.assertTrue(random_position.x >= 0 and random_position.x <= 800)
        self.assertTrue(random_position.y >= 0 and random_position.y <= 600)

    def test_get_random_velocity(self):
        """
        Test that get_random_velocity works as expected.
        """
        # Test getting a random velocity with min and max speeds
        min_speed = 10
        max_speed = 20
        random_velocity = get_random_velocity(min_speed, max_speed)
        self.assertTrue(random_velocity.magnitude() >= min_speed)
        self.assertTrue(random_velocity.magnitude() <= max_speed)

    def test_print_text(self):
        """
        Test that print_text works on a mock surface.
        """
        # Mock get_size method of Surface
        surface = MagicMock()
        surface.get_size.return_value = (800, 600)

        # Test printing text with new lines
        text = "Hello\nWorld"
        print_text(surface, text, self._font)
        surface.blit.assert_called()

        # Test printing text without new lines
        text = "Hello World"
        print_text(surface, text, self._font)
        surface.blit.assert_called()


if __name__ == "__main__":
    unittest.main()
