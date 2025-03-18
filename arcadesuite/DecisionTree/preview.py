from scobi import Environment
from pathlib import Path
from Decisiontree import Decisiontree
from utils import getViper
from nicegui import ui

game = "Boxing"
reward = "env" #"human"
       
model, features = getViper(game, reward)
temp = Decisiontree(model, features)
ret = temp.get_random_path()
ui.html(ret)
ui.run(title='DecisionTree')

