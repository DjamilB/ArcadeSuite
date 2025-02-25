from scobi import Environment
from pathlib import Path
from Decisiontree import Decisiontree
from utils import getViper
from nicegui import ui

game = "Skiing"
reward = "human" #"env"

def get_feature_names (game, reward):
    env_str = f"ALE/{game}-v5"

    ff_file_path = Path(f"../SCoBots/resources/checkpoints/{game}_seed0_reward-{reward}_oc_pruned")
    pruned_ff_name = f"pruned_{game.lower()}.yaml"

    env = Environment(env_str,
                    focus_dir=ff_file_path,
                    focus_file=pruned_ff_name,
                    hide_properties=False,
                    draw_features=True,
                    reward=0) 

    return env.get_vector_entry_descriptions()          

model = getViper(f"{game}_seed0_reward-{reward}_oc_pruned-extraction")
temp = Decisiontree(model, get_feature_names(game,reward))
ret = temp.getRandomPath()
with ui.row():
        ui.label(ret).style('white-space: pre-wrap; word-wrap: break-word;')
ui.run(title='DecisionTree')

