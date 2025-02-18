import os
<<<<<<< HEAD
import sys
import pytest
import json
from ocatari.core import OCAtari, AVAILABLE_GAMES

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from arcadesuite.utils import get_games, get_json


=======
import pytest
import json
from utils import get_games, get_json
from ocatari.core import OCAtari, AVAILABLE_GAMES

>>>>>>> 3c15e3e53945a9ed0b3c61a2d76a9fb13e6bfa20

def load_metadata(game_name):
    meta_path = f"arcadesuite/res/{game_name}/meta.json"
    with open(meta_path) as f:
        return json.load(f)
    
def test_game_modifs():
<<<<<<< HEAD
    GAMES = get_games() #TODO(artjom): fix path
=======
    global select_index

    GAMES = get_games()
    selected_game = GAMES[select_index]
>>>>>>> 3c15e3e53945a9ed0b3c61a2d76a9fb13e6bfa20

    for game in GAMES:
        meta = load_metadata(game)
        if meta["modifs"]["change_enemy"] == "ce":
<<<<<<< HEAD
            env = OCAtari(game)
            ram_before = env.get_ram()
            env.step()
            ram_after = env.get_ram()
            assert ram_before != ram_after
            
        if meta["modifs"]["change_player"] == "cp":
            env = OCAtari(game)

        #TODO(artjom): add tests for other modifs ...S
=======
            game_instance = OCAtari(game)
            #TODO(artjom): add test for change_enemy
            
        #TODO(artjom): add tests for other modifs
>>>>>>> 3c15e3e53945a9ed0b3c61a2d76a9fb13e6bfa20


if __name__ == "__main__":
    pytest.main()