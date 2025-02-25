import os
import json


def get_games():
    path = "../res/games.json"
    if os.path.isfile(path):
        with open(path, "r") as file:
            games = json.load(file)
            return games["games"]
    else:
        raise FileNotFoundError(f"The file {path} does not exist.")


def get_json(path):
    file = open(path, "r")
    contents = file.read()
    return json.loads(contents)


def map_to_pygame_key_codes(keycode):
    return {
        "e": 101,
        " ": 32,
        "w": 119,
        "a": 97,
        "s": 115,
        "d": 100,
    }.get(str(keycode), 0)
