import numpy as np
from graphviz import Digraph
from treeElements import action_dict


class Feature:
    def __init__(self, index, featurename = None):
        self.featurename = featurename
        self.index = index
        self.lower_bound = None
        self.upper_bound = None

    def set_upper_bound(self, bound):
        if self.upper_bound is None:
            self.upper_bound = bound
        elif bound < self.upper_bound:
            self.upper_bound = bound

    def set_lower_bound(self, bound):
        if self.lower_bound is None:
            self.lower_bound = bound
        elif bound > self.lower_bound:
            self.lower_bound = bound

    def get_bound(self):
        temp = False
        width = 10  # Einheitliche Breite für Zahlen & "Unknown"
        middle_width = 12  # Breite für x[...] (zentriert)

        if self.featurename is None:
            element = f"x[{self.index}]"
        else:
            element = f"{self.featurename}"

        # Formatierung der unteren Grenze
        if self.lower_bound is not None:
            lower = f"{self.lower_bound: .2f}".rjust(width) + " \033[31m<=\033[0m "
            temp = True
        else:
            lower = "-\u221e".rjust(width) + " \033[31m<=\033[0m "

        # Formatierung der oberen Grenze
        if self.upper_bound is not None:
            upper = f" \033[31m<\033[0m {self.upper_bound: .2f}".ljust(width + 6)
            temp = True
        else:
            upper = f" \033[31m<\033[0m \u221e".ljust(width + 6)

        if temp:
            return lower + element.center(middle_width) + upper
        else:
            return None


        
class BinaryDotTree:
    def __init__(self, model, featurenames= None):
        self.model = model
        self.featurenames = featurenames

    def traverse(self, node_id, nodes, obs, features, tabs, ret):
        if node_id < 0 or self.model.tree_.feature[node_id]<0 :
            #print(ret)
            return ret, (tabs-1)
        feature = self.model.tree_.feature[node_id]
       
        # If featureIndex not already exists create new feature
        if feature not in features: 
            temp = Feature(feature, self.featurenames[feature])
        else: 
            temp = features[feature]

        threshold = self.model.tree_.threshold[node_id]

        # if obs[feature] <= threshold: Do leftchild Next (True) 
        if obs[feature] <= threshold:
            temp.set_upper_bound(threshold)
            ret = ret + "\t" * tabs + f"{self.featurenames[feature]}\033[90m({obs[feature]: .2f})\033[0m \033[31m <= \033[0m {threshold: .2f}\n"
            features[feature] = temp
            left_child = self.model.tree_.children_left[node_id]
            if self.values_change(node_id, nodes):
                return self.traverse(left_child, nodes, obs, features, tabs + 1, ret)
            else:
                return ret, tabs
            
        # if obs[feature] > threshold: do rightChild Next (False)
        else:
            temp.set_lower_bound(threshold)
            ret = ret + "\t" * tabs + f"{self.featurenames[feature]}\033[90m({obs[feature]: .2f})\033[0m \033[31m > \033[0m {threshold: .2f}\n"
            features[feature] = temp
            right_child = self.model.tree_.children_right[node_id]
            if self.values_change(node_id, nodes):
                return self.traverse(right_child, nodes, obs, features, tabs + 1, ret)
            else: 
                return ret, tabs
            
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

    def values_change(self, current, nodes):
        start = nodes.index(current)
        current_value = self.get_value(nodes[start])
        temp = False
        for element in nodes[start+1:]:
            if self.get_value(element) != current_value: 
                return True
        return temp

    def get_value(self,node_id):
       values = np.round(self.model.tree_.value[node_id], 2)
       return  action_dict[np.argmax(values)]

    def getPath(self, obs):
        nodes = self.getDecision(obs)
        features = dict()
        ret,tabs = self.traverse(0,nodes, obs, features, 0,"")
        ret = ret + "\n" + f"Choosen Action: \033[31m {self.get_value(nodes[-1])}\033[0m \n"
        ret = ret + "\n" + "Feature Evaluation:" 
        for feat in features.values():
            ret = ret + "\n" + "\t" + feat.get_bound()
        
        print(ret)
    
    def getRandomPath(self):
        random_obs = np.random.rand(self.model.n_features_in_)* 20 - 10
        print("Number Of Features", self.model.n_features_in_)
        return self.getPath(random_obs)









   