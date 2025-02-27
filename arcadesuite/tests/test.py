import os
import sys
import json


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from arcadesuite.utils import get_games, get_json


def load_metadata(game_name):
    meta_path = f"arcadesuite/res/{game_name}/meta.json"
    with open(meta_path) as f:
        return json.load(f)