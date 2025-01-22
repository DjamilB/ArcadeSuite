import os
import json


def get_games(path):
    games = list()
    for d in os.listdir(path):
        if os.path.isdir(path + d):
            games.append(d)
    return games


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
