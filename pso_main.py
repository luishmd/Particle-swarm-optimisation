__author__ = "Luis Domingues"
__maintainer__ = "Luis Domingues"
__email__ = "luis.hmd@gmail.com"

#----------------------------------------------------------------------------------------
# Notes
#----------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------
import sys
import os
import lib_path_ops
import yaml
import pso_classes as pso


#----------------------------------------------------------------------------------------
    # PRE-CALCULATIONS
#----------------------------------------------------------------------------------------
# Get inputs
root_dir = os.getcwd()
root_dir = root_dir+'/'


#----------------------------------------------------------------------------------------
# FUNCTIONS
#----------------------------------------------------------------------------------------
def get_parameters(root_dir):
    """
    Function that reads the yaml inputs config file and returns a dictionary with all the parameters
    :param root_dir: directory of execution
    :return: dictionary containing all the parameters needed to run the script
    """
    # Get inputs from inputs.yaml
    try:
        input_file = lib_path_ops.join_paths(root_dir, 'inputs/inputs.yaml')
        with open(input_file, 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        search_space_dic = cfg['Decision variables']
        main_params_dic = cfg['Main parameters']

        params_dic = main_params_dic

        print("Loaded inputs successfully.")
        return search_space_dic, params_dic
    except:
        print("Failed to load inputs. Exiting...")
        sys.exit(1)



#----------------------------------------------------------------------------------------
# EXECUTION
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    search_space, params_dic = get_parameters(root_dir)
    pso_alg = pso.pso(search_space, params_dic)
    pso_alg.execute()