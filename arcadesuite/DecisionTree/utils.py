import numpy as np
from joblib import load
from scobi import Environment
from pathlib import Path
import os
import sys

action_dict = {
    0: "NOOP",
    1: "FIRE",
    2: "UP",
    3: "RIGHT",
    4: "LEFT",
    5: "DOWN",
    6: "UPRIGHT",
    7: "UPLEFT",
    8: "DOWNRIGHT",
    9: "DOWNLEFT",
    10: "UPFIRE",
    11: "RIGHTFIRE",
    12: "LEFTFIRE",
    13: "DOWNFIRE",
    14: "UPRIGHTFIRE",
    15: "UPLEFTFIRE",
    16: "DOWNRIGHTFIRE",
    17: "DOWNLEFTFIRE"
}

def get_viper(game, reward, seed):
    base_path = f"../ScoBots/resources/viper_extracts/extract_output/{game}_seed{seed}_reward-{reward}_oc_pruned-extraction"
    file_name = None
    for file in os.listdir(base_path):
        if file.endswith("_best.viper"):
            file_name = file
            break
    
    if file_name:
        file_path = os.path.join(base_path, file_name)
        print("\t\033[32m[Load Viper Tree]\033[0m Tree found!")
    else: 
        print("\t\033[32m[Load Viper Tree]\033[0m Tree not Found!")

    return load(file_path)

def get_features(game, reward, seed):
    env_str = f"ALE/{game}-v5"

    ff_file_path = Path(f"../ScoBots/resources/checkpoints/{game}_seed{seed}_reward-{reward}_oc_pruned")
    pruned_ff_name = f"pruned_{game.lower()}.yaml"
    
    if not ff_file_path.exists():        
        print("\t\033[32m[Load Featurenames]\033[0m Names not Found!")
        return None
    else:
        print("\t\033[32m[Load Featurenames]\033[0m Names Found!")
        sys.stdout = open(os.devnull, 'w')
        env = Environment(env_str,
                focus_dir=ff_file_path,
                focus_file=pruned_ff_name,
                hide_properties=False,
                draw_features=True, 
                reward=0) 
        sys.stdout = sys.__stdout__
        return env.get_vector_entry_descriptions() 

def get_Decisiontree_data(game, reward, seed):
    """
    Retrieves the Viper decision tree and feature descriptions for a given game and reward-type.

    This function searches for a Viper tree file with the best performance within a specified directory 
    and attempts to load feature names from a corresponding file. If successful, it returns the loaded 
    Viper tree and feature descriptions.

    Args:
        game (str): The name of the game for which the Viper tree is being retrieved.
        reward (str): The reward type (human or env)

    Returns:
        tuple: A tuple containing:
            - dict: The loaded Viper decision tree (or None if not found).
            - list or None: A list of feature descriptions if available, otherwise None.

    Prints:
        Messages indicating whether the Viper tree and feature names were found or not.
    """
 
    model = get_viper(game, reward, seed)

    if model:
        features = get_features(game, reward, seed)

        return model, features
    else:
        print("No Viper Tree found!\n Try viper_extract")  
        return None, None
       