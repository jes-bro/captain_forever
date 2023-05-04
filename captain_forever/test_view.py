import pytest
import view
import pygame


@pytest.mark.parametrize(
    "actual_value,expected_value", pygame.display.get_init()
)
def test_display_initialization(actual_value, expected_value):
    """
    Check that the various initial display properties have been initialized to
    the correct values.

    Args:
        actual_value: A tuple containing the initialized display property.
        expected_value: A tuple containing the expected value for the property.
    """
    assert actual_value == expected_value


@pytest.fixture
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


def test_print_text(pygame_init):
    """
    Test the print_text function with real Pygame Surface and Font objects
    and checks if the message has been rendered on the surface by looking for
    the presence of the expected color in the surface's pixels.

    Args:
        pygame_init: A pytest fixture that initializes and cleans up the Pygame library.
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

    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            if surface.get_at((x, y))[:3] == expected_color[:3]:
                found_expected_color = True
                break

    assert found_expected_color, "Text not found in the rendered surface"
