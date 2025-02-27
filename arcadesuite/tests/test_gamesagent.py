import pytest
from game_page import populate
from test import get_games, load_metadata


def test_game_modifs():
    GAMES = get_games()
    