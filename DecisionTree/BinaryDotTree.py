import numpy as np
from graphviz import Digraph
from treeElements import action_dict


class NodeElement:
    def __init__(self, id, feature, threshold, values):
        self.id = id
        self.feature = feature
        self.threshold = threshold
        self.values = values

    def get_id(self):
        return self.id
    
    def getActionOfValues(self):
        return action_dict[np.argmax(self.values)]
    
    def get_label(self):
        return f"x[{self.feature}] <= {self.threshold: .2f} \\n {self.values}"

class EdgeElement:
    def __init__(self, label, start, end):
        self.label = label
        self.start = start
        self.end = end

    def get_label(self):
        return self.label

    def get_start(self):
        return self.start
    
    def get_end(self):
        return self.end

class BinaryDotTree:
    def __init__(self, model):
        self.model = model
        self.node_data = []              #Nodes
        self.edge_data = [None]          #Edges (Start with None, so that for i>0:   edge_i leads to  node_i )
        self.previous = []
        self.initLists(0)

    def initLists(self, node_id):
        if node_id == -1:
            return

        feature = self.model.tree_.feature[node_id]         
        threshold = self.model.tree_.threshold[node_id]
        values = np.round(self.model.tree_.value[node_id], 2)

        node = NodeElement(node_id, feature, threshold, values[0])

        self.node_data.append(node)

        left_child = self.model.tree_.children_left[node_id]
        right_child = self.model.tree_.children_right[node_id]

        # Recursive call 
        if left_child != -1:
            edge = EdgeElement("True", node_id, left_child)            
            self.edge_data.append(edge)  
            self.initLists(left_child)

        if right_child != -1:
            edge = EdgeElement("False", node_id, right_child)            
            self.edge_data.append(edge)     
            self.initLists(right_child)

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

    def getPath(self, obs):
        nodes = self.getDecision(obs)
        length = len(nodes)-1
        dot = Digraph()
        dot.attr('node', shape='box', style='rounded', color='black', fontname='helvetica')
        dot.attr(size="5,10")
        dot.attr(ratio="fill")
        #dot.attr('graph', rankdir='LR')
        dot.attr('edge', fontname='helvetica')

        for i in nodes:
            if i==nodes[length]:
                dot.attr('node', shape='box', fontname='helvetica', style='filled')
                dot.node(f"{self.node_data[i].get_id()}", label=self.node_data[i].getActionOfValues(), fillcolor='red')
                dot.edge(f"{self.edge_data[i].get_start()}", f"{self.edge_data[i].get_end()}", label=f"{self.edge_data[i].get_label()}" ,color="black")

            else: 
                dot.node(f"{self.node_data[i].get_id()}", label=f"{self.node_data[i].get_label()}", color="black")
                if i!=0:
                    dot.edge(f"{self.edge_data[i].get_start()}", f"{self.edge_data[i].get_end()}", label=f"{self.edge_data[i].get_label()}" ,color="black")
        return dot


    def getTree(self, obs):
        nodes = self.getDecision(obs)

        dot = Digraph()
        dot.attr('node', shape='box', style='rounded', color='black', fontname='helvetica')
        dot.attr('graph', rankdir='LR') # Allginment Left to Right 
        dot.attr(size="10,20")
        dot.attr(ratio="fill")
        #dot.attr('graph', ranksep = 'equally', splines='polyline')
        dot.attr('edge', fontname='helvetica')

        for i in range(len(self.node_data)):
            if i in nodes:
                dot.node(f"{self.node_data[i].get_id()}", label ="", color="red")
                if i != 0: 
                    dot.edge(f"{self.edge_data[i].get_start()}", f"{self.edge_data[i].get_end()}",label ="", color="red")

            else:
                dot.node(f"{self.node_data[i].get_id()}", label ="", color="black") 
                if i != 0: 
                    dot.edge(f"{self.edge_data[i].get_start()}", f"{self.edge_data[i].get_end()}", label ="", color="black")
        return dot

    def getRandomTree(self):
        random_obs = np.random.rand(self.model.n_features_in_)* 20 - 10
        return self.getTree(random_obs) 
    
    def getRandomPath(self):
        random_obs = np.random.rand(self.model.n_features_in_)* 20 - 10
        return self.getPath(random_obs)









   