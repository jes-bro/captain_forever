"""
Test the ArrowController class to respond appropriately to key inputs.
"""
import pytest
import pygame
import math
from pygame import Vector2
from game import CaptainForever
from models import Bullet, Ship, GameObject, NPCShip, StaticObject
from utils import load_sprite

test_game = CaptainForever()
surface = test_game.screen
test_object = GameObject(
    Vector2(0), load_sprite("ship", True, True), Vector2(0))

GameObject_init_cases = [
    # Check if GameObject attributes initialized to the right type.
    (test_object.velocity, pygame.Vector2),
    (test_object.sprite, pygame.Surface),
    (test_object.radius, float),
]
GameObject_collide_cases = [
    # check if GameObject methods perform the right operations
    # Does a game object collide with an object that is on top of it
    (GameObject(test_object.position, load_sprite(
        "ship", True, True), Vector2(0)), True),
    (StaticObject(test_object.position, "fire"), True),
    (Bullet(test_object.position, Vector2(0)), True),
    (Ship(test_object.position, test_game.bullets.append, "ship", True, True), True),
    (NPCShip(test_object.position, "ship", test_game.bullets.append), True),

    # Does a game object collide with an object that is far from it
    (StaticObject(test_object.position + \
     Vector2(test_object.radius)*10, "fire"), False),
    (Bullet(test_object.position + Vector2(test_object.radius)*10, Vector2(0)), False),
    (Ship(test_object.position + Vector2(test_object.radius)
     * 10, test_game.bullets.append, "ship", True, True), False),
    (NPCShip(test_object.position + Vector2(test_object.radius)
     * 10, "ship", test_game.npc_bullets.append), False),

    #  does a game object collide with an object that is located at its edge
    (StaticObject(test_object.position + Vector2(test_object.radius), "fire"), True),
    (Bullet(test_object.position + Vector2(test_object.radius), Vector2(0)), False),
    (Ship(test_object.position + Vector2(test_object.radius),
     test_game.bullets.append, "ship", True, True), True),
    (NPCShip(test_object.position + Vector2(test_object.radius),
     "ship", test_game.bullets.append), True),
]

GameObject_move_cases = [
    # Check the distance a game object is moving with move is correct after setting velocity
    (Vector2(1, 0), 1),
    (Vector2(0, 1), 1),
    (Vector2(100, 0), 100),
    (Vector2(0, 100), 100),
    # test that velocities over the width of the screen get positions wrapped around
    (Vector2(surface.get_width() + 100, 0), 100),
    (Vector2(0, surface.get_height() + 100), 100),
]

test_ship = Ship(
    (400, 400), test_game.bullets.append, "player", True, False
)
ship_init_cases = [
    # Check if GameObject attributes initialized to the right type.
    (test_ship._health, int),
    (test_ship.direction, pygame.Vector2),
    (test_ship.sprite, pygame.Surface),
    (test_ship.ACCELERATION, float),
    (test_ship.BULLET_SPEED, int),
    (test_ship.MANEUVERABILITY, int),
]

ship_rotate_degrees_cases = [
    # Check that rotating does not change magnitude of direction vector
    (True,  test_ship.MANEUVERABILITY),
    (False, test_ship.MANEUVERABILITY * -1),
]

ship_accelerate_decellerate_cases = [
    # Check that accelerating/decellerating by 1 changes magnitude of
    # velocity by ACCELERATION
    (1, test_ship.ACCELERATION),
    (-1, test_ship.ACCELERATION),
    # test that accelerating/decellerating by 3 changes magnitude of
    # velocity by 3* ACCELERATION
    (3, test_ship.ACCELERATION * 3),
    (-3, test_ship.ACCELERATION * 3)
]

# Test _process_game_logic
ship_reduce_health_cases = [
    # check that the reduce health function only reduces the amount of health by 1
    (1)

]


@ pytest.mark.parametrize("attribute, attribute_type", GameObject_init_cases)
def test_object_init_cases(attribute, attribute_type):
    """
    Check if GameObjects are initialized with attributes of the correct type.

    velocity should be a Vector2, sprite should be a surface, and radius should be a float

    Args:
        attribute: An attribute of the GameObject.
        attribute_type: The type of the attribute.
    """

    # Check if attribute is of the correct type.
    assert isinstance(attribute, attribute_type)


@ pytest.mark.parametrize("collider, collision_bool", GameObject_collide_cases)
def test_collide_cases(collider, collision_bool):
    """
    Check if the key press to move results in the correct action.

    If the arrow keys are pressed down, call the move method in the ship class.

    Args:
        attribute: An attribute of the game instance.
        attribute_type: The type of the attribute.
    """
    # Check if attribute is of the correct type.
    assert test_object.collides_with(collider) == collision_bool


@ pytest.mark.parametrize("velocity, distance_change", GameObject_move_cases)
def test_move_cases(velocity, distance_change):
    """
    # Check the distance a game object is moving with move is correct after setting velocity

    Args:
        velocity: Vector2 of x and y pixels that object should move on move method.
        distance_change: expected magnitude (number of pixels) of that move.
    """
    original_position = test_object.position
    test_object.velocity = velocity
    test_object.move(surface)
    new_position = test_object.position

    assert original_position.distance_to(new_position) == distance_change


@ pytest.mark.parametrize("attribute, attribute_type", ship_init_cases)
def test_ship_init_cases(attribute, attribute_type):
    """
    Check if Ship instances are initialized with attributes of the correct type.

    velocity should be a Vector2, sprite should be a surface, and radius should be a float

    Args:
        attribute: An attribute of the GameObject.
        attribute_type: The type of the attribute.
    """

    # Check if attribute is of the correct type.
    assert isinstance(attribute, attribute_type)


@ pytest.mark.parametrize("clockwise_bool, expected_change", ship_rotate_degrees_cases)
def test_ship_rotate_degrees_cases(clockwise_bool, expected_change):
    """
    Check if Ship rotation method is modifying direction by the right angle.

    Vector2 direction should  change by  expected_change degrees

    Args:
        clockwise_bool: bool, tells the rotation whether it is clockwise
        expected_change: int, number of degrees the rotation is expected to be
    """
    test_ship.direction = Vector2(0, -1)
    test_ship.rotate(clockwise_bool)
    actual_change = math.ceil(Vector2(0, -1).angle_to(test_ship.direction))

    # Check if direction has changed by the correct number of degrees.
    assert actual_change == expected_change


@ pytest.mark.parametrize("acceleration_value, expected_change", ship_accelerate_decellerate_cases)
def test_ship_accelerate_decellerate_cases(acceleration_value, expected_change):
    """
    Check if Ship accellerate/decellerate method is modifying attributes by the correct amount.

    Vector2 attributes of velocity should change by the ACCELERATION factor  

    Args:

    """
    test_ship.velocity = Vector2(0)
    if acceleration_value < 0:
        acceleration_value = acceleration_value * -1
        test_ship.deccelerate(acceleration_value)
    else:
        test_ship.accelerate(acceleration_value)
    actual_change = test_ship.velocity.magnitude()

    # Check if attribute is of the correct type.
    assert expected_change == actual_change


# TODO: shoot and move(NPC) testing, redo rotation testing,
