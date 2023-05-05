# pylint: disable=no-member
# pylint: disable=no-name-in-module
# pylint: disable=protected-access
# Disabling pylint warnings related to PyGame that aren't valid
# Disabling protected access because we need to modify private vars to test
# certain conditions
"""
Test the print_text function in the view class using pytest.
"""
import pygame
import view


def test_print_text():
    """
    Test the print_text function with real Pygame Surface and Font objects
    and checks if the message has been rendered on the surface by looking for
    the presence of the expected color in the surface's pixels.
    """
    # Create a real Pygame Surface object
    surface = pygame.Surface((800, 600))

    text = "Test message"

    # Create a real Pygame Font object
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    view.print_text(surface, text, font)

    # Check if the text is present in the rendered surface by
    # checking for the presence of the expected color.
    expected_color = pygame.Color("tomato")
    found_expected_color = False

    for x_position in range(surface.get_width()):
        for y_position in range(surface.get_height()):
            if (
                surface.get_at((x_position, y_position))[:3]
                == expected_color[:3]
            ):
                found_expected_color = True
                break

        if found_expected_color:
            break

    assert found_expected_color, "Text not found in the rendered surface"
