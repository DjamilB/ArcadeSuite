import numpy as np
from DecisionTree.utils import action_dict
from nicegui import ui

# HTML constants
red = '<span style="color: red";>'
gray = '<span style="color: gray";>'
end = '</span>'

class Feature:
    def __init__(self, index, featurename = None):
        self.featurename = featurename or f"x[{index}]"
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
    
    def get_name(self):
        return self.featurename

    def get_bound(self):
        temp = False
        width = 10  
        middle_width = 14  
        operator_width = 4  

        # Formated lower Bound
        if self.lower_bound is not None:
            lower = f"{self.lower_bound: .2f}".rjust(width) + red + " <= " + end
            temp = True
        else:
            lower = "-\u221e".rjust(width) + red + " <= " + end

        # Formated upper Bound
        if self.upper_bound is not None:
            upper = red + " < " + end + f"{self.upper_bound: .2f}".ljust(width)
            temp = True
        else:
            upper = red + " < " + end + f" \u221e".ljust(width)

        # Allignment
        lower = lower.rjust(width + operator_width)
        upper = upper.rjust(width + operator_width)

        if temp:
            return f"<pre>{lower}{self.featurename.center(middle_width + 7)}{upper}</pre>"
        else:
            return None

class Decisiontree:
    def __init__(self, model, featurenames= None):
        self.model = model
        self.featurenames = featurenames

    def traverse(self, node_id, nodes, obs, features, tabs, ret):
        if node_id < 0 or self.model.tree_.feature[node_id]<0 :
            return ret, (tabs-1)
        feature = self.model.tree_.feature[node_id]
       
        # If featureIndex not already exists create new feature
        if feature not in features:
            if self.featurenames:
                temp = Feature(feature, self.featurenames[feature])
            else: 
                temp = Feature(feature)
        else: 
            temp = features[feature]

        threshold = self.model.tree_.threshold[node_id]

        # if obs[feature] <= threshold: do left child Next (True) 
        if obs[feature] <= threshold:
            temp.set_upper_bound(threshold)
            ret = ret + "&nbsp;&nbsp;&nbsp;&nbsp;" * tabs + f"{temp.get_name()}({gray}{obs[feature]: .2f}{end}) {red} <= {end}  {threshold: .2f}<br>"
            features[feature] = temp
            left_child = self.model.tree_.children_left[node_id]
            if self.values_change(node_id, nodes):
                return self.traverse(left_child, nodes, obs, features, tabs + 1, ret)
            else:
                return ret, tabs
            
        # if obs[feature] > threshold: do right child Next (False)
        else:
            temp.set_lower_bound(threshold)
            ret = ret + "&nbsp;&nbsp;&nbsp;&nbsp;" * tabs + f"{temp.get_name()}({gray}{obs[feature]: .2f}{end}) {red} > {end} {threshold: .2f}<br>"
            features[feature] = temp
            right_child = self.model.tree_.children_right[node_id]
            if self.values_change(node_id, nodes):
                return self.traverse(right_child, nodes, obs, features, tabs + 1, ret)
            else: 
                return ret, tabs
            
    def get_decision(self, obs):
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

    def get_path(self, obs):
        nodes = self.get_decision(obs)
        features = dict()
        ret,tabs = self.traverse(0,nodes, obs, features, 0,"<pre><b>Decisions:</b><br>")
        ret = ret + "<br>" + f"<b>Choosen Action: {red} {self.get_value(nodes[-1])} {end} </b><br>"
        ret = ret + "<br>" + "<b>Feature Evaluation:</b>" 
        
        for feat in features.values():
            ret = ret + "&nbsp;&nbsp;&nbsp;&nbsp;" + feat.get_bound() 
        
        return ret +"</pre>"
    
    def get_random_path(self):
        random_obs = np.random.rand(self.model.n_features_in_)* 20 - 10
        return self.getPath(random_obs)









   
