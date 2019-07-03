__author__ = "Luis Domingues"
__maintainer__ = "Luis Domingues"
__email__ = "luis.hmd@gmail.com"

#----------------------------------------------------------------------------------------
# Notes
#----------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------
import random as rand




#----------------------------------------------------------------------------------------
# BOUND FUNCTIONS
#----------------------------------------------------------------------------------------
def reset_to_bounds(search_space, position, seed=None):
    """
    Function that resets the position to the bounds if these are violated.
    """
    rand.seed(a=seed)
    position_bounded = {}
    vars_names = search_space.get_variables_names()
    for v in vars_names:
        var_type = search_space.get_variable_type(v)
        if var_type == 'int' or var_type == 'float':
            lb = search_space.get_variable_lbound(v)
            ub = search_space.get_variable_ubound(v)
            if (position[v] >= lb) and (position[v] <= ub):
                position_bounded[v] = position[v]
            elif (position[v] >= ub):
                position_bounded[v] = ub
            else:  # position[v] <= lb
                position_bounded[v] = lb
        elif var_type == 'enumerate':
            values = search_space.get_variable_values(v)
            if position[v] in values:
                position_bounded[v] = position[v]
            else:
                position_bounded[v] = values[rand.randint(len(values))]
        elif var_type == 'binary':
            if position[v] in [0, 1]:
                position_bounded[v] = position[v]
            else:
                position_bounded[v] = rand.randint(2)
        else:
            print("Could not enforce bounds for variable {}".format(v))
    return position_bounded

