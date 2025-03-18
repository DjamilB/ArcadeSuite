import numpy as np
from joblib import load
from scobi import Environment
from pathlib import Path
import os

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

def getViper(game, reward):
    base_path = f"../SCoBots/resources/viper_extracts/extract_output/{game}_seed0_reward-{reward}_oc_pruned-extraction"
    file_name = None
    for file in os.listdir(base_path):
        if file.endswith("_best.viper"):
            file_name = file
            break

    if file_name:
        file_path = os.path.join(base_path, file_name)
        print("Viper Tree found!")

        env_str = f"ALE/{game}-v5"

        ff_file_path = Path(f"../SCoBots/resources/checkpoints/{game}_seed0_reward-{reward}_oc_pruned")
        pruned_ff_name = f"pruned_{game.lower()}.yaml"

        if not ff_file_path.exists():        
            print(f"No Featurenames found...")
            features = None
        else:
            env = Environment(env_str,
                    focus_dir=ff_file_path,
                    focus_file=pruned_ff_name,
                    hide_properties=False,
                    draw_features=True, 
                    reward=0) 
            
            features = env.get_vector_entry_descriptions() 

        return load(file_path), features 
    
    else:
        print("No Viper Tree found!\n Try viper_extract")  
        return None, None
       