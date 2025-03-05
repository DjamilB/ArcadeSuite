import os
import json
import ale_py
from ocatari.utils import _load_checkpoint, partial, _epsilon_greedy, PPOAgent, AtariNet, QNetwork, PPO_Obj_small

try:
    import torch
    from torch import nn
    from torch.distributions.categorical import Categorical
    torch_imported = True
except ModuleNotFoundError:
    torch_imported = False
    

head_html = '''
            <link rel="preconnect" href="https://fonts.googleapis.com" />
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
            <link href="https://fonts.googleapis.com/css2?family=VT323&display=swap" rel="stylesheet" />
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


def load_multiplayer_agent(opt, agent, env=None, device="cpu"):
    pth = opt if isinstance(opt, str) else opt.path
    if "dqn" in pth or "c51" in pth:
        agent = AtariNet(env.action_spaces[agent].n, distributional="c51" in pth)
        ckpt = _load_checkpoint(pth)
        agent.load_state_dict(ckpt['estimator_state'])
        policy = partial(_epsilon_greedy, model=agent)
        return agent, policy
    elif "cleanrl" in pth:
        if device == "cpu":
            ckpt = torch.load(pth, map_location=torch.device('cpu'))
        else:
            ckpt = torch.load(pth)
        if "c51" in pth:
            agent = QNetwork(env.action_space.n)
            agent.load_state_dict(ckpt["model_weights"])
        elif "ppo" in pth and env.obs_mode == "dqn":
            agent = PPOAgent(env)
            agent.load_state_dict(ckpt["model_weights"])
        elif "ppo" in pth and env.obs_mode == "obj":
            agent = PPO_Obj_small(env, len(env.ns_state),
                                  env.buffer_window_size, device)
            agent.load_state_dict(ckpt["model_weights"])
        else:
            return None

        policy = agent.draw_action

    return agent, policy
