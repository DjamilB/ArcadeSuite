import os
import json
import ale_py
from arcadesuite import load_agent
from ocatari import utils
    

head_html = '''
            <link rel="preconnect" href="https://fonts.googleapis.com" />
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
            <link href="https://fonts.googleapis.com/css2?family=VT323&display=swap" rel="stylesheet" />
            <style>
                html, body {
                    background-color: bisque;
                    overflow: hidden;                   
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


def get_keys_to_action_p1() -> dict[tuple[int, ...], ale_py.Action]:
    UP = "w"
    LEFT = "a"
    RIGHT = "d"
    DOWN = "s"
    FIRE = " "
    NOOP = "e"

    mapping = {
        ale_py.Action.NOOP: (NOOP,),
        ale_py.Action.UP: (UP,),
        ale_py.Action.FIRE: (FIRE,),
        ale_py.Action.DOWN: (DOWN,),
        ale_py.Action.LEFT: (LEFT,),
        ale_py.Action.RIGHT: (RIGHT,),
        ale_py.Action.UPFIRE: (UP, FIRE),
        ale_py.Action.DOWNFIRE: (DOWN, FIRE),
        ale_py.Action.LEFTFIRE: (LEFT, FIRE),
        ale_py.Action.RIGHTFIRE: (RIGHT, FIRE),
        ale_py.Action.UPLEFT: (UP, LEFT),
        ale_py.Action.UPRIGHT: (UP, RIGHT),
        ale_py.Action.DOWNLEFT: (DOWN, LEFT),
        ale_py.Action.DOWNRIGHT: (DOWN, RIGHT),
        ale_py.Action.UPLEFTFIRE: (UP, LEFT, FIRE),
        ale_py.Action.UPRIGHTFIRE: (UP, RIGHT, FIRE),
        ale_py.Action.DOWNLEFTFIRE: (DOWN, LEFT, FIRE),
        ale_py.Action.DOWNRIGHTFIRE: (DOWN, RIGHT, FIRE),
    }

    return {
        tuple(sorted(mapping[act_idx])): act_idx for act_idx in range(18)
    }


def get_keys_to_action_p2() -> dict[tuple[int, ...], ale_py.Action]:
    UP = "ArrowUp"
    LEFT = "ArrowLeft"
    RIGHT = "ArrowRight"
    DOWN = "ArrowDown"
    FIRE = "Control"
    NOOP = "Shift"

    mapping = {
        ale_py.Action.NOOP: (NOOP,),
        ale_py.Action.UP: (UP,),
        ale_py.Action.FIRE: (FIRE,),
        ale_py.Action.DOWN: (DOWN,),
        ale_py.Action.LEFT: (LEFT,),
        ale_py.Action.RIGHT: (RIGHT,),
        ale_py.Action.UPFIRE: (UP, FIRE),
        ale_py.Action.DOWNFIRE: (DOWN, FIRE),
        ale_py.Action.LEFTFIRE: (LEFT, FIRE),
        ale_py.Action.RIGHTFIRE: (RIGHT, FIRE),
        ale_py.Action.UPLEFT: (UP, LEFT),
        ale_py.Action.UPRIGHT: (UP, RIGHT),
        ale_py.Action.DOWNLEFT: (DOWN, LEFT),
        ale_py.Action.DOWNRIGHT: (DOWN, RIGHT),
        ale_py.Action.UPLEFTFIRE: (UP, LEFT, FIRE),
        ale_py.Action.UPRIGHTFIRE: (UP, RIGHT, FIRE),
        ale_py.Action.DOWNLEFTFIRE: (DOWN, LEFT, FIRE),
        ale_py.Action.DOWNRIGHTFIRE: (DOWN, RIGHT, FIRE),
    }

    return {
        tuple(sorted(mapping[act_idx])): act_idx for act_idx in range(18)
    }


class FakeEnv:
    def __init__(self, observation_space, action_space, obs_mode):
        self.observation_space = observation_space
        self.action_space = action_space
        self.obs_mode = obs_mode

def custom_load_agent(opt, name, env=None, is_multiplayer=False, device="cpu"):
    if is_multiplayer:
        if env.unwrapped.obs_type == "grayscale_image":
            obs_mode = "dqn"
        elif env.unwrapped.obs_type == "rgb_image":
            obs_mode = "ori"
        else:
            # don't know if oc agents will work
            obs_mode = "obj"

        env = FakeEnv(env.observation_space(name), env.action_space(name), obs_mode)

    pth = opt if isinstance(opt, str) else opt.path

    if "dqn" in pth or "c51" in pth:
        return utils.load_agent(opt, env, device)
    else:
        return load_agent.load_agent(opt, env, device)