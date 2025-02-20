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
    match keycode:
        case "e":
            return 101
        case " ":
            return 32
        case "w":
            return 119
        case "a":
            return 97
        case "s":
            return 115
        case "d":
            return 100
        case _:
            return 0
