# pylint: disable=no-member
"""
Test the ArrowController class to respond appropriately to key inputs.
"""
import pytest
import pygame
from game import CaptainForever
from models import Ship, NPCShip, StaticObject

pygame.init()
width = 1082
height = 720
screen = pygame.display.set_mode((width, height))
test_game = CaptainForever(1082, 720)

init_cases = [
    # Check if game class attributes are initialized to the right type.
    (test_game.message, str),
    (test_game.counter, int),
    (test_game.fires, list),
    (test_game.npc_ships, list),
    (test_game.npc_bullets, list),
    (test_game.bullets, list),
    (test_game.is_running, bool),
    (test_game.player_ship, Ship),
    (test_game.enemy_spawn_counter, int),
]
# Test _process_game_logic
test_player_ship_pos = (50, 50)
test_initial_player_ship_pos = (400, 400)
test_far_pos = (800, 800)
test_cases = [
    # Test case 1: No message, process game objects and no collision
    ([
        # List of game objects
        # bullets, npc_bullets, npc_ships
        [], [], [NPCShip(test_far_pos, "ship", test_game.bullets.append)],
    ], "continue"),  # expected result

    # Test case 2: Player collides with npc_ship
    ([
        # bullets, npc_bullets, npc_ships
        [], [], [NPCShip(test_initial_player_ship_pos,
                         "ship", test_game.bullets.append)],
    ], "lost"),  # expected result

    # Test case 3: No npc ships left and player ship still alive
    ([
        [], [], [],  # bullets, npc_bullets, npc_ships
    ], "won"),  # expected result

    # ... additional test cases ...
]


@ pytest.mark.parametrize("attribute, attribute_type", init_cases)
def test_init_cases(attribute, attribute_type):
    """
    Check if the key press to move results in the correct action.

    If the arrow keys are pressed down, call the move method in the ship class.

    Args:
        attribute: An attribute of the game instance.
        attribute_type: The type of the attribute.
    """

    # Check if attribute is of the correct type.
    test_game.__init__(1082, 720)
    assert isinstance(attribute, attribute_type)


def test_enemy_ship_spawning():
    """
    Check that correct number of enemy ships are added to game upon init.
    """
    test_game.__init__(width, height)
    assert len(test_game.npc_ships) == 3


@pytest.mark.parametrize("game_objects, expected_result", test_cases)
def test_process_game_logic(game_objects, expected_result):
    # unpack game objects
    bullets, npc_bullets, npc_ships = game_objects

    # replace game object lists with input game objects
    test_game._bullets = bullets
    test_game._npc_bullets = npc_bullets
    test_game._npc_ships = npc_ships

    # call _process_game_logic method
    test_game._process_game_logic()

    # check that the expected game state was reached
    if expected_result == "continue":
        assert test_game.message_flag == ""
    elif expected_result == "lost":
        assert isinstance(test_game.player_ship, StaticObject)
        assert test_game.message_flag == "lost"
    elif expected_result == "won":
        assert test_game.message_flag == "won"
    else:
        raise ValueError(f"Invalid expected_result: {expected_result}")

# get game objects, end game message, spawn enemy
