# pylint: disable=no-member
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

pygame.init()
width = 1082
height = 720
surface = pygame.display.set_mode((width, height))
test_game = CaptainForever(width, height)
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
    (Vector2(width + 100, 0), 100),
    (Vector2(0, height + 100), 100),
]


# Ship test cases
test_game.test_ship = Ship(
    (400, 400), test_game.bullets.append, "player", True, False
)
ship_init_cases = [
    # Check if GameObject attributes initialized to the right type.
    (test_game.test_ship._health, int),
    (test_game.test_ship.direction, pygame.Vector2),
    (test_game.test_ship.sprite, pygame.Surface),
    (test_game.test_ship.ACCELERATION, float),
    (test_game.test_ship.BULLET_SPEED, int),
    (test_game.test_ship.MANEUVERABILITY, int),
]

ship_rotate_degrees_cases = [
    # Check that rotating does not change magnitude of direction vector
    (True,  test_game.test_ship.MANEUVERABILITY),
    (False, test_game.test_ship.MANEUVERABILITY * -1),
]

ship_accelerate_decellerate_cases = [
    # Check that accelerating/decellerating by 1 changes magnitude of
    # velocity by ACCELERATION
    (1, test_game.test_ship.ACCELERATION),
    (-1, test_game.test_ship.ACCELERATION),
    # test that accelerating/decellerating by 3 changes magnitude of
    # velocity by 3* ACCELERATION
    (3, test_game.test_ship.ACCELERATION * 3),
    (-3, test_game.test_ship.ACCELERATION * 3)
]

ship_reduce_health_cases = [
    # Check that repeated calls to reduce_health result in correct health values
    # uses get_health function, this acts as a test for reduce_health and get_health methods
    (1, 2),
    (2, 1),
    (3, 0),
]

ship_shoot_cases = [
    # Check that ship shoot method appends a bullet object to the game bullets list each time it is called
    (1, 1),
    (2, 2),
    (3, 3)
]

# NPC ship test cases
# keep in mind for these tests that the test_game.test_ship (player ship) is at (400, 400) so a ship at
# (0, 0) with a direction (heading) of (1, 1) is pointed DIRECTLY towards the player ship.
npc_move_shoot_cases = [
    # check to see whether the NPC shoots on move at correct cases (should only shoot with heading towards player)
    ((-1, -1), 0),
    # this heading is towards the player
    ((1, 1), 1),
    # different magnitude of the same player facing heading
    ((.5, .5), 1),
    # heading away from the player
    ((-.5, -.5), 0),
    # heading away from the player
    ((1, 0), 0)
]

# testing whether the move method of NPC's rotates the direction in appropriate cases (checks method flag)
npc_move_rotate_cases = [
    # rotates on imperfect heading
    ((-1, -1), 4),
    ((-1, 1), 4),
    ((-1, 0), 4),
    # does not rotate on perfect heading
    ((1, 1), 8),
    ((.5, .5), 8)
]

# Check NPC velocities are being altered correctly for different cases in move
npc_move_velocity_cases = [
    # rotates but has zero velocity if not facing the player
    ((-1, -1), (400, 399), True),
    ((-1, 1), (0, 0), True),
    ((-1, 0), (0, 0), True),
    # on perfect heading velocity is modified if above 300 units away or under 150
    ((1, 1), (400, 399), True),
    ((.5, .5), (0, 0), False),
    # on perfect heading between 300 and 150 units away, no velocity
    ((1, 0), (200, 400), True)

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
    test_object._velocity = velocity
    test_object.move(width, height)
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
    test_game.test_ship._direction = Vector2(0, -1)
    test_game.test_ship.rotate(clockwise_bool)
    actual_change = math.ceil(
        Vector2(0, -1).angle_to(test_game.test_ship.direction))

    # Check if direction has changed by the correct number of degrees.
    assert actual_change == expected_change


@ pytest.mark.parametrize("acceleration_value, expected_change", ship_accelerate_decellerate_cases)
def test_ship_accelerate_decellerate_cases(acceleration_value, expected_change):
    """
    Check if Ship accellerate/decellerate method is modifying attributes by the correct amount.

    Vector2 attributes of velocity should change by the ACCELERATION factor  

    Args:
        acceleration_value: int, number to multiply ACCELERATION by to accelerate. If negative, calls decellerate
        expected_change: float, expected difference in magnitude between original and new velocity vector
    """
    test_game.test_ship._velocity = Vector2(0)
    if acceleration_value < 0:
        acceleration_value = acceleration_value * -1
        test_game.test_ship.deccelerate(acceleration_value)
    else:
        test_game.test_ship.accelerate(acceleration_value)
    actual_change = test_game.test_ship.velocity.magnitude()

    # Check if velocity has changed by the magnitude expected.
    assert expected_change == actual_change


@ pytest.mark.parametrize("times_to_reduce, expected_health", ship_reduce_health_cases)
def test_ship_reduce_health_cases(times_to_reduce, expected_health):
    """
    Check if Ship reduce_health method is reducing health by 1 on repeated calls.

    This test validates both reduce_health and get_health methods to modify and access the
    private property _health

    Args:
        times_to_reduce: int, number of times to reduce the player health by 1
        expected_health: int, health expected after number of reductions (starts at 3)
    """
    test_game.test_ship._health = 3
    for _ in range(times_to_reduce):
        test_game.test_ship.reduce_health()

    # Check if health is the correct value.
    assert test_game.test_ship.get_health() == expected_health


@ pytest.mark.parametrize("times_to_shoot, number_of_bullets", ship_shoot_cases)
def test_ship_shoot_cases(times_to_shoot, number_of_bullets):
    """
    Check that Ship shoot method creates and appends to a list a bullet object every call.

    The length of the test_game.bullets list should be equal to the number of times shoot called

    Args:
        times_to_shoot: int, number of times the player ship shoots a bullet
        number_of_bullets: int, new bullets in the bullets list
    """
    starting_bullets = len(test_game.bullets)
    for _ in range(times_to_shoot):
        test_game.test_ship.shoot()
    bullet_instances = len(test_game.bullets)-starting_bullets

    # Check if health is the correct value.
    assert bullet_instances == number_of_bullets


@ pytest.mark.parametrize("heading, shots", npc_move_shoot_cases)
def test_npc_move_shoot_cases(heading, shots):
    """
    Check that NPC shoots on move method call at correct cases (should only shoot with heading towards player, 
    3 deg variance)

    keep in mind for these tests that the test_game.test_ship (player ship) is at (400, 400) so a ship at 
    (0, 0) with a direction (heading) of (1, 1) is pointed DIRECTLY towards the player ship.

    Args:
        heading: tuple, vector of the heading of an NPC, (1, 1) is towards the player
        shots: int, new bullets in list. Should be 1 for cases where NPC should shoot
    """
    starting_bullets = len(test_game.npc_bullets)
    test_game.npc_ship = (NPCShip(Vector2(0), "ship", test_game.npc_bullets.append)
                          )
    test_game.npc_ship._direction = Vector2(heading)
    # forcing the shooting delay above its threshold
    test_game.npc_ship._shooting_delay = 1100
    test_game.npc_ship.move(test_game.test_ship, width, height)
    bullet_instances = len(test_game.npc_bullets) - starting_bullets

    # Check if health is the correct value.
    assert bullet_instances == shots


@ pytest.mark.parametrize("heading, move_flag", npc_move_rotate_cases)
def test_npc_move_rotate_cases(heading, move_flag):
    """
    Check that NPC rotates on move method call at correct cases (should only rotate with heading not towards
    player, 3 deg variance)

    keep in mind for these tests that the test_game.test_ship (player ship) is at (400, 400) so a ship at 
    (0, 0) with a direction (heading) of (1, 1) is pointed DIRECTLY towards the player ship.

    Args:
        heading: tuple, vector of the heading of an NPC, (1, 1) is towards the player
        direction_change: bool, whether direction vector is the same as it started
    """
    test_game.npc_ship = (NPCShip(Vector2(0), "ship", test_game.npc_bullets.append)
                          )
    test_game.npc_ship._direction = Vector2(heading)
    # forcing the shooting delay above its threshold
    test_game.npc_ship.move(test_game.test_ship, width, height)
    # Check if health is the correct value.
    assert move_flag == test_game.npc_ship.method_flag


@ pytest.mark.parametrize("heading, npc_position, velocity_change", npc_move_velocity_cases)
def test_npc_move_velocity_cases(heading, npc_position, velocity_change):
    """
    Check that NPC changes velocity on move method call at correct cases (should only modify velocity 
    with heading toward player, and outside of a 150 and 300 pixels away window

    keep in mind for these tests that the test_game.test_ship (player ship) is at (400, 400) so a ship at 
    (0, 0) with a direction (heading) of (1, 1) is pointed DIRECTLY towards the player ship.

    Args:
        heading: tuple, vector of the heading of an NPC, (1, 1) is towards the player
        velocity_change: bool, whether direction vector is the same as it started
    """
    test_game.npc_ship = (NPCShip(Vector2(0), "ship", test_game.npc_bullets.append)
                          )
    test_game.npc_ship._direction = Vector2(heading)
    test_game.npc_ship._position = Vector2(npc_position)
    test_game.npc_ship._velocity = Vector2(0)
    # forcing the shooting delay above its threshold
    test_game.npc_ship.move(test_game.test_ship, width, height)
    change_bool = test_game.npc_ship.velocity == Vector2(0)
    # Check if health is the correct value.
    assert velocity_change == change_bool
