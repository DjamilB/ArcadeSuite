import numpy as np
from .utils import action_dict

# HTML-Constants
red = '<span style="color: red";>'      # Operator
gray = '<span style="color: gray";>'    # Observation
end = '</span>'
tabs = '&nbsp;&nbsp;&nbsp;&nbsp;'       # Tabs

class Feature:
    """
    Represents a feature in the decision tree with updated boundaries.
    """
      
    def __init__(self, index, featurename = None):
        """
        Initializes a Feature object.

        Args:
            index (int): The index of the feature.
            featurename (str, optional): The name of the feature. Defaults to None.
        """
        self.index = index
        self.featurename = featurename or f"x[{index}]"
        self.lower_bound = None
        self.upper_bound = None

    def set_upper_bound(self, bound):
        """
        Updates the upper bound for the feature.

        Args:
            bound (float): The upper bound value.
        """
        self.upper_bound = min(self.upper_bound or bound, bound)

    def set_lower_bound(self, bound):
        """
        Updates the lower bound for the feature.

        Args:
            bound (float): The lower bound value.
        """
        self.lower_bound = max(self.lower_bound or bound, bound)
    
    def get_name(self):
        return self.featurename

    def get_bound(self):
        """
        Generates a formatted string representation of the feature bounds.

        Returns:
            str or None: An HTML formatted string of bounds, or None if no bounds are set.
        """
        temp = False
        width = 10  
        middle_width = 14  
        operator_width = 4  

        if self.lower_bound is not None:
            lower = f"{self.lower_bound: .2f}".rjust(width) + red + " <= " + end
            temp = True
        else:
            lower = "-\u221e".rjust(width) + red + " <= " + end

        if self.upper_bound is not None:
            upper = red + " < " + end + f"{self.upper_bound: .2f}".ljust(width)
            temp = True
        else:
            upper = red + " < " + end + f" \u221e".ljust(width)

        lower = lower.rjust(width + operator_width)
        upper = upper.rjust(width + operator_width)

        if temp:
            return f"<pre>{lower}{self.featurename.center(middle_width + 7)}{upper}</pre>"
        else:
            return None

class Decisiontree:
    """
    A class representing a decision tree for traversal and decision-making.
    """
    def __init__(self, model, featurenames= None):
        """
        Initializes a Decisiontree object.

        Args:
            model (object): A sklearn.DecisionTreeClassifier.
            featurenames (list, optional): A list of feature names. Defaults to None.
        """
        self.model = model
        self.featurenames = featurenames

    def traverse(self, node_id, nodes, obs, features, n_tabs, ret):
        """
        Traverses the decision tree recursively and formats the path.

        Args:
            node_id (int): Current node ID in the decision tree.
            nodes (list): List of visited nodes.
            obs (array): Observation data.
            features (dict): Dictionary of feature objects.
            n_tabs (int): Indentation level.
            ret (str): Accumulated formatted result.

        Returns:
            tuple: A tuple containing the formatted path and the indentation level.
        """
        if node_id < 0 or self.model.tree_.feature[node_id]<0:
            return ret, (n_tabs-1)
        feature = self.model.tree_.feature[node_id]
        
        if feature not in features:
            if self.featurenames:
                temp = Feature(feature, self.featurenames[feature])
            else: 
                temp = Feature(feature)
        else: 
            temp = features[feature]

        threshold = self.model.tree_.threshold[node_id]

        if obs[feature] <= threshold:
            temp.set_upper_bound(threshold)
            ret = ret + tabs * n_tabs + f"{temp.get_name()}({gray}{obs[feature]: .2f}{end}) {red} <= {end}  {threshold: .2f}<br>"
            features[feature] = temp
            left_child = self.model.tree_.children_left[node_id]
            if self.decision_change(node_id, nodes):
                return self.traverse(left_child, nodes, obs, features, n_tabs + 1, ret)
            else:
                return ret, n_tabs
            
        else:
            temp.set_lower_bound(threshold)
            ret = ret + tabs * n_tabs + f"{temp.get_name()}({gray}{obs[feature]: .2f}{end}) {red} > {end} {threshold: .2f}<br>"
            features[feature] = temp
            right_child = self.model.tree_.children_right[node_id]
            if self.decision_change(node_id, nodes):
                return self.traverse(right_child, nodes, obs, features, n_tabs + 1, ret)
            else: 
                return ret, n_tabs
            
    def get_decision(self, obs):
        """
        Determines the decision path for a given observation.

        Args:
            obs (array): Observation data.

        Returns:
            list: A list of nodes representing the decision path.
        """
        node_id = 0  
        nodes = []  

        while node_id != -1:  
            nodes.append(node_id)  

            threshold = self.model.tree_.threshold[node_id]
            feature_index = self.model.tree_.feature[node_id]
        
            if obs[feature_index] <= threshold:
                node_id = self.model.tree_.children_left[node_id]  
            else:
                node_id = self.model.tree_.children_right[node_id]  
        return nodes

    def decision_change(self, current, nodes):
        """
        Checks if the Decision change at a given node.

        Args:
            current (int): Current node ID.
            nodes (list): List of decision path nodes.

        Returns:
            bool: True if decision changes, otherwise False.
        """
        start = nodes.index(current)
        current_value = self.get_value(nodes[start])
        for element in nodes[start+1:]:
            if self.get_value(element) != current_value: 
                return True
        return False

    def get_value(self,node_id):
        """
        Gets the action value for a given node.

        Args:
            node_id (int): Node ID.

        Returns:
            str: The corresponding action value.
        """ 
        values = self.model.tree_.value[node_id]
        return  action_dict[np.argmax(values)]

    def get_path(self, obs):
        """
        Generates a decision path for a given observation.

        Args:
            obs (array): Observation data.

        Returns:
            str: A formatted HTML string representing the decision path.
        """
        nodes = self.get_decision(obs)
        features = dict()
        ret,_ = self.traverse(0,nodes, obs, features, 0,"<pre><b>DECISIONS:</b><br>")
        ret = ret + "<br>" + f"<b>CHOSEN ACTION: {red} {self.get_value(nodes[-1])} {end} </b><br>"
        ret = ret + "<br>" + "<b>FEATURE EVALUATION:</b>" 
        
        for feat in features.values():
            ret = ret + tabs + feat.get_bound() 
        
        return ret +"</pre>"









   
