import pytest
from game_page import populate
from test import get_games, load_metadata

    
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