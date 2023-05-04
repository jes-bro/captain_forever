"""
Test the ArrowController class to respond appropriately to key inputs.
"""
import pytest
import pygame as pg
from game import CaptainForever
from models import Ship
from controller import ArrowController

test_game = CaptainForever()
test_player = test_game.player_ship
test_player_controller = ArrowController(test_game)


game_initialize_cases = [
    # Test that when the game begins there is no end game message.
    ((test_game.message), ("")),
    # Test that the player is a Ship instance.
    ((isinstance(test_player, Ship)), (True)),
    # Test that counter has not iterated.
    ((test_game.counter), (0)),
    # Test that enemy spawn counter has not been iterated
    ((test_game.enemy_spawn_counter), (0))
    # Test that NPC's are stored in a list
    ((isinstance(test_game.npc_ships), (list)))
    # Test that before game loop is run game is not running
    ((test_game.is_running), (False))
]


@pytest.mark.parametrize("actual_value,expected_value", game_initialize_cases)
def test_display_initialization(actual_value, expected_value):
    """
    Check that the various initial model properties have been initialized to
    the correct values.

    There should be no message, the player instance should be present, all counters
    should be equal to zero, NPC ships should be stored in a list, and the game should 
    not be running (main loop has not yet run).

    Args:
        actual_value: A tuple containing some data from the initialized property.
        expected_value: A tuple containing the expected value for the property's data.
    """
    assert actual_value == expected_value
