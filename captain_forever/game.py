# pylint: disable=no-member
# pylint: disable=no-name-in-module
# Disabling pylint warnings related to PyGame that aren't valid
"""
Game class that processes the game logic in our model.
"""
from utils import get_random_position
from models import Ship, NPCShip, StaticObject


class CaptainForever:
    """
    Class which processes game logic and interfaces with the view
    and controller classes.

    Attributes:
        counter: Int, counter that helps delay when fire disappears.
        _fires: List, elements are StaticObject instances.
        _npc_ships: List, elements are NPCShip instances.
        _npc_bullets: List, elements are Bullet instances from NPCShip instances.
        _bullets: List, elements are Bullet instances from player_ship.
        _player_ship: Ship instance representing player that responds to input.
        _enemy_spawn_counter: Int, iterated counter to keep track of spawning.
        _message_flag: String, tells you if you have won or lost the game.
        _message: A string representing the message to be displayed at end.
    """

    ENEMY_SPAWN_DISTANCE = 400

    def __init__(self, width, height):
        """
        Initialize captain forever game attributes.

        Args:
            width: Int, represents width of screen.
            height: Int, represents height of screen.
        """
        self._message = ""
        self._fires = []
        self._npc_ships = []
        self._npc_bullets = []
        self._bullets = []
        self.counter = 0
        self.player_ship = Ship(
            (400, 400), self._bullets.append, "player", True, False
        )
        self._width = width
        self._height = height
        self._enemy_spawn_counter = 0
        self._message_flag = ""
        for _ in range(3):
            while True:
                position = get_random_position(width, height)
                if (
                    position.distance_to(self.player_ship.position)
                    > self.ENEMY_SPAWN_DISTANCE
                ):
                    break
            # second argument specifies ship and not fire
            self._npc_ships.append(
                NPCShip(position, "ship", self._npc_bullets.append)
            )

    @property
    def message(self):
        """
        Return _message.

        Returns:
            _message: A string representing the message to be displayed at end.
        """
        return self._message

    @property
    def fires(self):
        """
        Return _fires.

        Returns:
            _fires: List, elements are StaticObject instances.
        """
        return self._fires

    @property
    def bullets(self):
        """
        Return _bullets.

        Returns:
            _bullets: List, elements are bullet instances.
        """
        return self._bullets

    @property
    def npc_bullets(self):
        """
        Return _npc_bullets.

        Returns:
            _npc_bullets: List, elements are bullet instances.
        """
        return self._npc_bullets

    @property
    def npc_ships(self):
        """
        Return _npc_ships.

        Returns:
            _npc_ships: List, elements are NPCShip instances.
        """
        return self._npc_ships

    @property
    def enemy_spawn_counter(self):
        """
        Return _enemy_spawn_counter.

        Returns:
            _enemy_spawn_counter: Int, represents a value that
            helps determine when to spawn more enemies in.
        """
        return self._enemy_spawn_counter

    @property
    def message_flag(self):
        """
        Return _message_flag.

        Returns:
            _message_flag: Bool, helps determine whether function
            was called in a unit test or not.
        """
        return self._message_flag

    @property
    def is_running(self):
        """
        Return _is_running.

        Returns:
            _is_running: Bool, helps us determine whether game is
            running or not.
        """
        return isinstance(self.player_ship, Ship)

    @property
    def width(self):
        """
        Return _width.

        Returns:
            _width: Int, width of screen.
        """
        return self._width

    @property
    def height(self):
        """
        Return _height.

        Returns:
            _height: Int, height of screen.
        """
        return self.height

    def main_loop(self, controller, view):
        """
        Run main loop that updates PyGame screen frames
        to keep game running, updating the screen based
        on user input and the changes in our model state.

        Args:
            controller: An instance of ArrowController.
            view: An instance of PyGame view.
        """
        while True:
            controller.maneuver_player_ship()
            self._process_game_logic()
            view.draw()

    def get_game_objects(self):
        """
        Return all game objects that have not been destroyed.

        Returns:
            game_objects: List of all game objects as class instances.
        """
        game_objects = [
            *self._npc_ships,
            *self._bullets,
            *self._npc_bullets,
            *self._fires,
        ]

        if self.player_ship:
            game_objects.append(self.player_ship)
        return game_objects

    def _process_game_logic(self):
        """
        Process movement, collisions, and game state on non-destroyed game objects.
        """
        if not self._message:
            for game_object in self.get_game_objects():
                if (
                    game_object in self._npc_ships
                ):  # or game_object in self._fires:
                    game_object.move(
                        self.player_ship, self._width, self._height
                    )
                elif (
                    game_object in self._bullets
                    or game_object in self._npc_bullets
                ):
                    game_object.move()
                else:
                    game_object.move(self._width, self._height)
            for npc_ship in self._npc_ships:
                if npc_ship.collides_with(self.player_ship):
                    self.player_ship = StaticObject(
                        self.player_ship.position, "fire"
                    )
                    self._message_flag = "lost"
                    self._end_game_message()
                    # What would be nice is if it paused for a sec and returned to a start menu
                    break
            if len(self._npc_ships) < 8:
                self._enemy_spawn_counter += 5
                # enemy spawning scales with number of enemies left
                if self._enemy_spawn_counter > len(self._npc_ships) * 125:
                    self._enemy_spawn_counter = 0
                    self._spawn_enemy()

        # Check for bullet not hitting anything
        for bullet in self._bullets[:]:
            if (
                bullet.position.x > self._width
                or bullet.position.y > self._height
                or bullet.position.x < 0
                or bullet.position.y < 0
            ):
                self._bullets.remove(bullet)

        for bullet in self._npc_bullets[:]:
            if (
                bullet.position.x > self._width
                or bullet.position.y > self._height
                or bullet.position.x < 0
                or bullet.position.y < 0
            ):
                self._npc_bullets.remove(bullet)

        # Check for bullet collisions with npc ships
        for bullet in self._bullets[:]:
            for npc_ship in self._npc_ships[:]:
                if npc_ship.collides_with(bullet):
                    position_on_screen = npc_ship.position
                    self._npc_ships.remove(npc_ship)
                    fire = StaticObject(position_on_screen, "fire")
                    self._fires.append(fire)

        for bullet in self._npc_bullets[:]:
            if self.player_ship.collides_with(bullet) and self.is_running:
                self._npc_bullets.remove(bullet)
                self.player_ship.reduce_health()
                if self.player_ship.get_health() == 0:
                    self.player_ship = StaticObject(
                        self.player_ship.position, "fire"
                    )
                    self._message_flag = "lost"
                    self._end_game_message()

        if not self._npc_ships and self.player_ship:
            self._message_flag = "won"
            self._end_game_message()

    def _end_game_message(self):
        """
        Create the game _message and indicate whether the player won or lost.
        """
        self._message = (
            f"You {self._message_flag}! \n To exit, press escape \n To start a"
            " new game, press enter"
        )

    def _spawn_enemy(self):
        """
        Spawn in new enememy ship.
        """
        while True:
            position = get_random_position(self._width, self._height)
            if (
                position.distance_to(self.player_ship.position)
                < self.ENEMY_SPAWN_DISTANCE
            ):
                break
            # second argument specifies ship and not fire
            self._npc_ships.append(
                NPCShip(position, "ship", self._npc_bullets.append)
            )
