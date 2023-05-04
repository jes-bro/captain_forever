import pygame
import unittest
from unittest.mock import MagicMock
from pygame import Surface
from pygame.font import SysFont
from utils import load_sprite, wrap_position, get_random_position, get_random_velocity
from view import print_text


class TestMyModule(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1082, 720))
        self.font = pygame.font.Font(None, 64)

    def test_load_sprite(self):
        # Test loading a sprite with alpha and without scaling
        sprite = load_sprite("ship", with_alpha=True, with_scaling=False)
        self.assertIsNotNone(sprite)

        # Test loading a sprite without alpha and with scaling
        sprite = load_sprite("space_background",
                             with_alpha=False, with_scaling=True)
        self.assertIsNotNone(sprite)

    # def test_load_sound(self):
    #     # Test loading a sound
    #     sound = load_sound("laser")
    #     self.assertIsNotNone(sound)

    def test_wrap_position(self):
        # Test wrapping position that is off the top of the screen
        position = (-50, -50)
        surface = Surface((800, 600))
        wrapped_position = wrap_position(position, surface)
        self.assertEqual(wrapped_position, (750, 550))

        # Test wrapping position that is off the right of the screen
        position = (850, 300)
        surface = Surface((800, 600))
        wrapped_position = wrap_position(position, surface)
        self.assertEqual(wrapped_position, (50, 300))

        # Test wrapping position that is off the bottom of the screen
        position = (400, 650)
        surface = Surface((800, 600))
        wrapped_position = wrap_position(position, surface)
        self.assertEqual(wrapped_position, (400, 50))

        # Test wrapping position that is off the left of the screen
        position = (-50, 300)
        surface = Surface((800, 600))
        wrapped_position = wrap_position(position, surface)
        self.assertEqual(wrapped_position, (750, 300))

    def test_get_random_position(self):
        # Mock get_width and get_height methods of Surface
        surface = MagicMock()
        surface.get_width.return_value = 800
        surface.get_height.return_value = 600

        # Test getting a random position
        random_position = get_random_position(surface)
        self.assertTrue(random_position.x >= 0 and random_position.x <= 800)
        self.assertTrue(random_position.y >= 0 and random_position.y <= 600)

    def test_get_random_velocity(self):
        # Test getting a random velocity with min and max speeds
        min_speed = 10
        max_speed = 20
        random_velocity = get_random_velocity(min_speed, max_speed)
        self.assertTrue(random_velocity.magnitude() >= min_speed)
        self.assertTrue(random_velocity.magnitude() <= max_speed)

    def test_print_text(self):
        # Mock get_size method of Surface
        surface = MagicMock()
        surface.get_size.return_value = (800, 600)

        # Test printing text with new lines
        text = "Hello\nWorld"
        print_text(surface, text, self.font)
        surface.blit.assert_called()

        # Test printing text without new lines
        text = "Hello World"
        print_text(surface, text, self.font)
        surface.blit.assert_called()


if __name__ == '__main__':
    unittest.main()
