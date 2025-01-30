import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
import matplotlib.animation as animation
from joblib import load
import numpy as np
import time
import os

class BinaryTreePlot:
    def __init__(self, model):
        self.model = model
        self.figure, self.ax = plt.subplots(figsize=(14, 10))
        self.ax.axis("on")
        
        self.node_plots = []        #Nodes
        self.edge_plots = [None]    #Edges (Start with None, so that for i>0:   edge_i leads to  node_i )
        self.previous_nodes = []

    def plot_tree(self):
        #Build Tree
        self.rec_plot_tree(0, 0.1, 0.5, 0.1, 0)
        self.figure.canvas.draw_idle()

    def repaint(self, obs):
        # Calculate Path for Observation in Decission Tree
        nodes = self.getDecision(obs)   # TODO Maybe there is already a function for that 
        self.recolour(nodes)
        self.figure.canvas.draw_idle()

    def getDecision(self, obs):
        node_id = 0  
        nodes = []  

        while node_id != -1:  # As long as we not visit a leaf
            nodes.append(node_id)  

            # Extract Trehsholf and Feature Index from Decision Tree
            threshold = self.model.tree_.threshold[node_id]
            feature_index = self.model.tree_.feature[node_id]
        
            # True -> Left child, False -> Right child
            if obs[feature_index] <= threshold:
                node_id = self.model.tree_.children_left[node_id]  
            else:
                node_id = self.model.tree_.children_right[node_id]  
        return nodes

    def recolour(self, nodes):
        #Coloring nodes and edges red, which arent red yet 
        for i in nodes:
            if ((self.previous_nodes == None) or (i not in self.previous_nodes)):
                self.node_plots[i].set_color('red')
                if(self.edge_plots[i]!= None):
                    self.edge_plots[i].set_color('red')
        
        #Coloring nodes and edges black, which arent included in recent Path 
        for i in self.previous_nodes:
            if i not in nodes:
                self.node_plots[i].set_color('black')
                self.edge_plots[i].set_color('black')
        self.previous_nodes = nodes

    def rec_plot_tree(self, node_id, x, y, y_offset, depth):
        if node_id == -1:
            return

        # Print Recent Node in front of Edges (zorder)
        node_plot = self.ax.scatter(x, y, color="black", zorder=2)  
        self.node_plots.append(node_plot) 

        left_child = self.model.tree_.children_left[node_id]
        right_child = self.model.tree_.children_right[node_id]

        # Calculate new Positions for children nodes
        next_x = x + 0.1
        left_y = y - y_offset / 2
        right_y = y + y_offset / 2 

        # Recursive call 
        if left_child != -1:
            edge_plot = self.ax.plot([x, next_x], [y, left_y], color="black", zorder=1)[0]
            self.edge_plots.append(edge_plot)  
            self.rec_plot_tree(left_child, next_x, left_y, y_offset / 2, depth + 1)

        if right_child != -1:
            edge_plot = self.ax.plot([x, next_x], [y, right_y], color="black", zorder=1)[0]
            self.edge_plots.append(edge_plot)  
            self.rec_plot_tree(right_child, next_x, right_y, y_offset / 2, depth + 1)

def getViper(game):
    base_path = f"../SCoBots/resources/viper_extracts/extract_output/{game}"
    file_name = None
    for file in os.listdir(base_path):
        if file.endswith("_best.viper"):
            file_name = file
            break
    
    if file_name:
        file_path = os.path.join(base_path,file_name)
        print("Viper Tree found!") 
        return load(file_path) 
    else:
        print("No Viper Tree found!")  
        return None

if __name__ == "__main__":
    # Load Decisiontree from Viper
    model = getViper("Pong_seed0_reward-human_oc_pruned-extraction")

    bt_plot = BinaryTreePlot(model)
    bt_plot.plot_tree()

    start_time = time.time()
    index = 0
    while time.time() - start_time < 60:
        random_obs = np.random.rand(model.n_features_in_)
        
        bt_plot.repaint(random_obs)
        print("Refresh ", index)
        
        index = index + 1     
        plt.pause(0.0000001)  

    plt.show()
