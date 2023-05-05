"""
Test the ArrowController class to respond appropriately to key inputs.
"""
import pytest
import pygame as pg
from game import CaptainForever
from controller import ArrowController

pg.init()
width = 1082
height = 720
screen = pg.display.set_mode((width, height))
test_game = CaptainForever(1082, 720)
test_player = test_game.player_ship
test_player_controller = ArrowController(test_game)

player_shoot_cases = [
    # Check if keydown on the spacebar results in shooting.
    (pg.event.Event(pg.KEYDOWN, key=pg.K_SPACE), 1),
]

player_translate_cases = [
    # Check if keydown on arrows results in translation
    (pg.event.Event(pg.KEYDOWN, key=pg.K_UP), 5),
    (pg.event.Event(pg.KEYDOWN, key=pg.K_DOWN), 6),
]

player_rotate_cases = [
    (pg.event.Event(pg.KEYDOWN, key=pg.K_RIGHT), 4),
    (pg.event.Event(pg.KEYDOWN, key=pg.K_LEFT), 4),
]

quit_case = [
    # Check if game is quit.
    (pg.event.Event(pg.QUIT), True),
    (pg.event.Event(pg.KEYDOWN, key=pg.K_ESCAPE), True),
]

restart_case = [
    # Check if game restarts.
    (pg.event.Event(pg.KEYDOWN, key=pg.K_RETURN), 0),
    (pg.event.Event(pg.KEYDOWN, key=pg.K_KP_ENTER), 0),
]


@pytest.mark.parametrize("pygame_event, translate_flag", player_translate_cases)
def test_player_translate_cases(pygame_event, translate_flag):
    """
    Check if the key press to move results in the correct action.

    If the arrow keys are pressed down, call the move method in the ship class.

    Args:
        pygame_event: A pygame event simulating the key press of an arrow key.
        flag_value: An integer indicating which Player method has been called.
    """
    # Simulate key press.
    test_player_controller.game._message = False
    pg.event.post(pygame_event)  # add the event to the queue

    # Check if correct method is called.
    test_player_controller.maneuver_player_ship(testing=True)
    assert test_player_controller.game.player_ship.method_flag == translate_flag


@pytest.mark.parametrize("pygame_event, rotate_flag", player_rotate_cases)
def test_player_rotate_cases(pygame_event, rotate_flag):
    """
    Check if the key press to move results in the correct action.

    If the arrow keys are pressed down, call the move method in the ship class.

    Args:
        pygame_event: A pygame event simulating the key press of an arrow key.
        flag_value: An integer indicating which Player method has been called.
    """
    # Simulate key press.
    test_player_controller.game._message = False
    pg.event.post(pygame_event)  # add the event to the queue

    # Check if correct method is called.
    test_player_controller.maneuver_player_ship(testing=True)
    print(f"Message: {test_player_controller.game.message}")
    assert test_player_controller.game.player_ship.method_flag == rotate_flag


@pytest.mark.parametrize("pygame_event, shoot_flag_val", player_shoot_cases)
def test_player_shooting_cases(pygame_event, shoot_flag_val):
    """
    Check if the key press to shoot results in the correct action.

    If the spacebar is pressed down, call the shoot method in the ship class.

    Args:
        pygame_event: A pygame event simulating the key press of the spacebar.
        flag_value: An integer indicating which Player method has been called.
    """
    # Simulate key press.
    pg.event.post(pygame_event)  # add the event to the queue

    # Check if correct method is called.
    test_player_controller.maneuver_player_ship(testing=True)
    assert test_player_controller.game.player_ship.method_flag == shoot_flag_val


@pytest.mark.parametrize("pygame_event, is_quitting", quit_case)
def test_quit_case(pygame_event, is_quitting):
    """
    Check if clicking escape or PyGame quitting to quit the game results in
    the correct action.

    If the button is pressed, call PyGame's quit() method.

    Args:
        pygame_event: A PyGame event simulating the button click to quit.
        is_running: A boolean indicating if the game is running.
    """
    # Simulate click to exit game.
    pg.event.post(pygame_event)  # add the event to the queue

    # Check if game stops running.
    assert test_player_controller.game.is_quitting == is_quitting


@pytest.mark.parametrize("pygame_event, flag_value", restart_case)
def test_player_restart_case(pygame_event, flag_value):
    """
    Check if the key press to move results in the correct action.

    If the arrow keys are pressed down, call the move method in the ship class.

    Args:
        pygame_event: A pygame event simulating the key press of an arrow key.
        flag_value: An integer indicating which Player method has been called.
    """
    # Simulate key press.
    test_player_controller.game._message = True
    pg.event.post(pygame_event)  # add the event to the queue

    # Check if correct method is called when lost or won message is displayed.
    test_player_controller.maneuver_player_ship()
    assert test_player_controller.game.player_ship.method_flag == flag_value
