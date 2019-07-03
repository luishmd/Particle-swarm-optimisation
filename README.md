# Background
Implement an easy to use particle swarm optimisation algorithm (pso) library, that is both easy to use and to customise.


# Description
A particle swarm optimisation algorithm is a stochastic optimisation technique that can be used in a wide range of applications, from the design of engineering equipment to the determination of optimal parameters of machine learning algorthms.

The current library has the following features:
1. Ability to easily specify a search space from a text file
2. Ability to easily specify parameters via a text file
3. Different functions for bounds violation handling and ability easily switch between them
4. Can write the results to an excel file, including statistics and the set of parameters used, without overwriting previous executions


## Output
Excel file with optimal point and evolution of swarm fitness with iterations. The excel file where results are stored is copied from a defined template (set in inputs.yaml), to a subdirectory in 'outputs/'. The current date_time is used to generate the name of the subdirectory and output file. This prevents accidental overwriting.

## Input data ( See file 'inputs.yaml')
1. Search space

    User-defined decision variables, including lower and upper bounds, as well as the variable type. Types supported are: float, int, enumerate and binary.

2. Main parameters
    - *opt_type*: type of optimisation -- Possible values: min / max --
    - *seed*: seed number to use when generating random numbers -- Possible values: int / None --
    - *model_function*: name of function to be optimised -- Possible values: str --
    - *swarm_size*: size of the swarm -- Possible values: positive int --
    - *max_iterations*: maximum number of iterations to be executed -- Possible values: positive int --
    - *synchronous*: 
    - *enforce_bounds*: 
    - *enforce_bounds_function*: 
    - *inertia_weight*:
    - *acceleration_constant_local*: 
    - *acceleration_constant_global*:  
    - *output_template*: name of the excel template for results -- Possible values: str --
    - *write_to_console*: determines whether results are written to the console or not -- Possible values: True / False --

# Bound functions implemented

- *reset_to_bounds*: Simple function that resets each variable to the closest bound


# Technologies used
Python3 including the libraries:

	- math
	- os
	- os.path
	- datetime
	- openpyxl
	- sys
	- copy
	- random


# Status
This work is still in development.


# Known issues


# Future enhancements
1. Add sql connectivity
2. Add more bound functions
3. Add more statistics (especially on operator performance)


# How to use it
1. Open *pso_main.py* and run it.


# How to customise it to your needs
1. Define a function in *model/models.py* and set model name in input parameters

2. Define a search space in the inputs file. This corresponds to the set of decision variables

3. Open *pso_main.py* and run it.