from game import CaptainForever
from controller import WASDController
if __name__ == "__main__":
    captain_forever_game_instance = CaptainForever()
    captain_forever_controller = WASDController(captain_forever_game_instance)
    captain_forever_game_instance.main_loop(captain_forever_controller)
