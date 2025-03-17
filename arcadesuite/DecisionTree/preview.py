from scobi import Environment
from pathlib import Path
from Decisiontree import Decisiontree
from utils import getViper
from nicegui import ui

game = "Boxing"
reward = "env" #"human"
       
model, features = getViper(game, reward)
temp = Decisiontree(model, features)
ret = temp.getRandomPath()
ui.html(ret)
ui.run(title='DecisionTree')

