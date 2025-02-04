from treeElements import getViper
from BinaryDotTree import BinaryDotTree
import graphviz

class DecisionTree:
    def __init__(self,game,):
        self.showPath = True
        self.game = game
        self.model = getViper(game)
        self.tree = BinaryDotTree(self.model)

    def render_dot(self,dot_text):
        dot_graph = graphviz.Source(dot_text)
        return dot_graph.pipe(format="svg").decode("utf-8")

    def updateRandom(self, container):
        if self.showPath:
            dot_code = str(self.tree.getRandomPath())
        else:
            dot_code = str(self.tree.getRandomTree())
        
        container.set_content(self.render_dot(dot_code))

    def update(self, container, obs):
        if self.showPath:
            dot_code = str(self.tree.getPath(obs))
        else:
            dot_code = str(self.tree.getTree(obs))
        
        container.set_content(self.render_dot(dot_code))

    def changeRenderMode(self):
        self.showPath = not self.showPath
