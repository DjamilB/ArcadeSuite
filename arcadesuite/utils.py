import os
import json

head_html = '''
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=VT323&display=swap" rel="stylesheet">
            <style>
                body {
                    background-color: bisque;
                    font-family: "VT323", monospace;
                    font-size: 18px;
                    font-weight: 400;
                    font-style: normal;
                }
            </style>
            '''


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
