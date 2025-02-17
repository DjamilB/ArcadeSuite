import numpy as np
from graphviz import Digraph
from treeElements import action_dict


class NodeElement:
    def __init__(self, id, feature, threshold, values):
        self.id = id
        self.feature = feature
        self.threshold = threshold
        self.values = values
        self.children = []

    def get_id(self):
        return self.id
    
    def set_left_child(self, child):
        self.children.insert(0,child)

    def set_right_child(self, child):
        self.children.insert(1,child)

    def get_children(self):
        return self.children
    
    def getActionOfValues(self):
        return action_dict[np.argmax(self.values)]
    
    def get_label(self):
        return f"x[{self.feature}] <= {self.threshold: .2f} \\n Action: {self.getActionOfValues()}"

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
        node.set_left_child(left_child)
        node.set_right_child(right_child)

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
        dot.attr('node', shape='box', style='rounded', color='black', fontname='Roboto', penwidth="2")
        dot.attr(ratio="fill")
        #dot.attr('graph', rankdir='LR')
        dot.attr('edge', fontname='Roboto')

        recent_node = self.node_data[0]
        dot.node(f"{self.node_data[0].get_id()}", label=self.node_data[0].get_label(), color="black")
        prev = nodes[0]

        for i in range(1,length+1):
            recent_node = nodes[i]

            if prev + 1 == recent_node: # Childnode is Left
                
                if i == length:
                    dot.attr('node', shape='box', fontname='Roboto', style='rounded, filled')
                    dot.node(f"{self.node_data[recent_node].get_id()}", label=f"Action: {self.node_data[recent_node].getActionOfValues()}", fillcolor="red")
                else: 
                    dot.node(f"{self.node_data[recent_node].get_id()}", label=self.node_data[recent_node].get_label(), color="black")
                dot.edge(f"{self.edge_data[recent_node].get_start()}", f"{self.edge_data[recent_node].get_end()}", label=f"{self.edge_data[recent_node].get_label()}" ,color="black")
                
                if self.node_data[prev].get_children()[1] != None:
                    dot.node(f"{self.node_data[recent_node].get_id()}_B", label="...", shape="triangle", color="black", fillcolor="white", style="")
                    dot.edge(f"{self.edge_data[recent_node].get_start()}", f"{self.edge_data[recent_node].get_end()}_B", label="False" ,color="black")

            else: # Childnode is Right
                if self.node_data[prev].get_children()[0] != None:
                    dot.node(f"{self.node_data[recent_node].get_id()}_A", label="...",shape="triangle", color="black", fillcolor="red", style="")
                    dot.edge(f"{self.edge_data[recent_node].get_start()}", f"{self.edge_data[recent_node].get_end()}_A", label="True" ,color="black")

                if i == length:
                    dot.attr('node', shape='box', fontname='Roboto', style='rounded, filled')
                    dot.node(f"{self.node_data[recent_node].get_id()}", label=f"Action: {self.node_data[recent_node].getActionOfValues()}", fillcolor="red")
                else: 
                    dot.node(f"{self.node_data[recent_node].get_id()}", label=self.node_data[recent_node].get_label(), color="black")               
                dot.edge(f"{self.edge_data[recent_node].get_start()}", f"{self.edge_data[recent_node].get_end()}", label=f"{self.edge_data[recent_node].get_label()}" ,color="black")
            prev = recent_node
        
        return dot


    def getTree(self, obs):
        nodes = self.getDecision(obs)

        dot = Digraph()
        dot.attr('node', shape='box', style='rounded, filled', color='black',fillcolor ="white",fontname='Roboto', penwidth="2")
        dot.attr('graph', rankdir='LR') # Allginment Left to Right 
        dot.attr(size="10,20")
        dot.attr(ratio="fill")
        #dot.attr('graph', ranksep = 'equally', splines='polyline')
        dot.attr('edge', fontname='Roboto')

        for i in range(len(self.node_data)):
            if i in nodes:
                dot.node(f"{self.node_data[i].get_id()}", label ="", tooltip=self.node_data[i].get_label(), color="red")
                if i != 0: 
                    dot.edge(f"{self.edge_data[i].get_start()}", f"{self.edge_data[i].get_end()}",label ="", edgetooltip=f"{self.edge_data[i].get_label()}", color="red")

            else:
                dot.node(f"{self.node_data[i].get_id()}", label ="",tooltip=self.node_data[i].get_label(), color="black") 
                if i != 0: 
                    dot.edge(f"{self.edge_data[i].get_start()}", f"{self.edge_data[i].get_end()}", label ="", edgetooltip=f"{self.edge_data[i].get_label()}", color="black")
        return dot

    def getRandomTree(self):
        random_obs = np.random.rand(self.model.n_features_in_)* 20 - 10
        return self.getTree(random_obs) 
    
    def getRandomPath(self):
        random_obs = np.random.rand(self.model.n_features_in_)* 20 - 10
        return self.getPath(random_obs)









   