__author__ = "Luis Domingues"
__maintainer__ = "Luis Domingues"
__email__ = "luis.hmd@gmail.com"

#----------------------------------------------------------------------------------------
# Notes
#----------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------
import math
import random as rand




#----------------------------------------------------------------------------------------
# BOUND FUNCTIONS
#----------------------------------------------------------------------------------------
def __enforce_solution_bounds(self, solution):
    solution_bounded = {}
    vars_names = self.search_space.get_variables_names()
    for v in vars_names:
        var_type = self.search_space.get_variable_type(v)
        if var_type == 'int' or var_type == 'float':
            lb = self.search_space.get_variable_lbound(v)
            ub = self.search_space.get_variable_ubound(v)
            if (solution[v] >= lb) and (solution[v] <= ub):
                solution_bounded[v] = solution[v]
            elif (solution[v] >= ub):
                solution_bounded[v] = ub
            else:  # solution[v] <= lb
                solution_bounded[v] = lb
        elif var_type == 'enumerate':
            values = self.search_space.get_variable_values(v)
            if solution[v] in values:
                solution_bounded[v] = solution[v]
            else:
                solution_bounded[v] = values[rand.randint(len(values))]
        elif var_type == 'binary':
            if solution[v] in [0, 1]:
                solution_bounded[v] = solution[v]
            else:
                solution_bounded[v] = rand.randint(2)
        else:
            print("Could not enforce bounds for variable {}".format(v))
    return solution_bounded

