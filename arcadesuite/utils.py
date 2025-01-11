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
