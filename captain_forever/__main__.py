from game import CaptainForever
from controller import ArrowController
from view import PyGameView

if __name__ == "__main__":
    captain_forever_game_instance = CaptainForever()
    captain_forever_controller = ArrowController(captain_forever_game_instance)
    captain_forever_view = PyGameView(captain_forever_game_instance)
    captain_forever_game_instance.main_loop(
        captain_forever_controller, captain_forever_view
    )
