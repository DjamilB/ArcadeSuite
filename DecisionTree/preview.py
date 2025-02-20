
from BinaryDotTree import BinaryDotTree
from treeElements import getViper

# Modell laden
model = getViper("Boxing_seed0_reward-env_oc_pruned-extraction")
temp = BinaryDotTree(model)
temp.getRandomPath()

