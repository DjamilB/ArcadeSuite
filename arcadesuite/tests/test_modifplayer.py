import os
import sys
import pytest
import json
from game_page import populate

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from arcadesuite.utils import get_games, get_json



def load_metadata(game_name):
    meta_path = f"arcadesuite/res/{game_name}/meta.json"
    with open(meta_path) as f:
        return json.load(f)
    
def test_game_modifs():
    GAMES = get_games() #TODO(artjom): fix path

    for game in GAMES:
        meta = load_metadata(game)
        if meta["modifs"]["change_enemy"] == "ce":
            env = populate(game, "", False, "", True, "")
            ram_before = env.get_ram()
            env = populate(game, "ce", False, "", True, "")
            ram_after = env.get_ram()
            assert ram_before != ram_after
            
        if meta["modifs"]["change_player"] == "cp":
            env = populate(game, "", False, "", True, "")
            ram_before = env.get_ram()
            env = populate(game, "cp", False, "", True, "")
            ram_after = env.get_ram()
            assert ram_before != ram_after
            

        #TODO(artjom): add tests for other modifs ...


if __name__ == "__main__":
    pytest.main()