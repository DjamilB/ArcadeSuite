import os


def get_games(path):
    games = list()
    for d in os.listdir(path):
        if os.path.isdir(path + d):
            if os.path.isfile(path + d + '/icon.png'):
                games.append(d)
    return games
