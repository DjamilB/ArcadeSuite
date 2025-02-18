import os
import pytest
import json
from utils import get_games, get_json
from ocatari.core import OCAtari, AVAILABLE_GAMES


def load_metadata(game_name):
    meta_path = f"arcadesuite/res/{game_name}/meta.json"
    with open(meta_path) as f:
        return json.load(f)
    
def test_game_modifs():
    global select_index

    GAMES = get_games()
    selected_game = GAMES[select_index]

    for game in GAMES:
        meta = load_metadata(game)
        if meta["modifs"]["change_enemy"] == "ce":
            game_instance = OCAtari(game)
            #TODO(artjom): add test for change_enemy
            
        #TODO(artjom): add tests for other modifs


if __name__ == "__main__":
    pytest.main()