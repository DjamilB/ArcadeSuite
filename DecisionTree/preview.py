from scobi import Environment
from BinaryDotTree import BinaryDotTree
from pathlib import Path
from treeElements import getViper

game = "Pong"

env_str = f"ALE/{game}-v5"
ff_file_path = Path(f"../SCoBots/resources/checkpoints/{game}_seed0_reward-human_oc_pruned")
pruned_ff_name = f"pruned_{game.lower()}.yaml"

env = Environment(env_str,
                  focus_dir=ff_file_path,
                  focus_file=pruned_ff_name,
                  hide_properties=False,
                  draw_features=True, # implement feature attribution
                  reward=0) #env reward only for evaluation
features = env.get_vector_entry_descriptions()          

# Modell laden
model = getViper(f"{game}_seed0_reward-human_oc_pruned-extraction")
temp = BinaryDotTree(model, features)
temp.getRandomPath()

