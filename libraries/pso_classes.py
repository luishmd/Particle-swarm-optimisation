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
import copy
import models
import pso_bound_functions as pso_bound
import datetime
import lib_directory_ops
import lib_path_ops
import lib_file_ops
import lib_excel_ops_openpyxl as lib_excel


#----------------------------------------------------------------------------------------
# CLASSES
#----------------------------------------------------------------------------------------
class Particle(object):
    """ Creates a particle class to be used in a swarm """
    def __init__(self, p_id, position, velocity):
        self.id = p_id
        self.position = position
        self.velocity = velocity
        self.fitness = None
        self.particle_best_position = position
        self.swarm_best_position = None

    def __str__(self):
        if self.fitness:
            return "Particle {} has fitness {}".format(self.id, self.fitness)
        else:
            return "Particle {} has fitness None".format(self.id)

    def copy(self):
        return copy.deepcopy(self)

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def get_fitness(self):
        return self.fitness

    def get_particle_best_position(self):
        return self.particle_best_position

    def get_swarm_best_position(self):
        return self.swarm_best_position

    def update_fitness(self, new_fitness):
        self.fitness = new_fitness
        return 0

    def update_position(self, new_position):
        self.position = new_position
        return 0

    def update_particle_best_position(self, new_position):
        self.particle_best_position = new_position
        return 0

    def update_swarm_best_position(self, new_position):
        self.swarm_best_position = new_position
        return 0

    def update_velocity(self, new_velocity):
        self.velocity = new_velocity
        return 0


class Search_space(object):
    """ Creates a search space """
    def __init__(self, search_space):
        self.search_space = search_space

    def get_number_variables(self):
        return len(self.search_space)

    def get_variables_names(self):
        return tuple(self.search_space.keys())

    def get_variable_type(self, var):
        try:
            return self.search_space[var]["Type"]
        except KeyError:
            return None

    def get_variable_lbound(self, var):
        try:
            return self.search_space[var]["LBound"]
        except KeyError:
            return None

    def get_variable_ubound(self, var):
        try:
            return self.search_space[var]["UBound"]
        except KeyError:
            return None

    def get_variable_values(self, var):
        try:
            return self.search_space[var]["Values"]
        except KeyError:
            return None


class Swarm(object):
    """ Creates a swarm, which is a collection of particles with extra functionality """
    def __init__(self, search_space, seed=None):
        self.size = 0
        self.particle_list = []
        self.N_evals = 0
        self.N_failed_evals = 0
        self.seed = seed
        self.search_space = search_space
        self.best_particle_so_far = None
        self.best_particle_current = None

    def __str__(self):
        s = "Size: {}\nSeed: {}\n".format(self.size, self.seed)
        for i in self.particle_list:
            s += i.__str__() + "\n"
        return s

    def copy(self):
        return copy.deepcopy(self)

    def get_seed(self):
        return self.seed

    def get_size(self):
        return self.size

    def get_search_space(self):
        return self.search_space

    def get_particle(self, p_id):
        return self.particle_list[p_id]

    def get_particles(self):
        return self.particle_list

    def get_best_particle_so_far(self):
        return self.best_particle_so_far

    def get_best_particle_current(self):
        return self.best_particle_current

    def initialise(self, swarm_size, f_bound, seed=None):
        rand.seed(a=seed)
        vars_names = self.search_space.get_variables_names()
        for i in range(swarm_size):
            # Initialise position
            position = {}
            for v in vars_names:
                var_type = self.search_space.get_variable_type(v)
                if var_type == 'int' or var_type == 'float':
                    lb = self.search_space.get_variable_lbound(v)
                    ub = self.search_space.get_variable_ubound(v)
                    position[v] = lb + (ub - lb)*rand.random()
                elif var_type == 'enumerate':
                    values = self.search_space.get_variable_values(v)
                    position[v] = values[rand.randint(0, len(values)-1)]
                elif var_type == 'binary':
                    position[v] = rand.randint(2)
                else:
                    print("Could not determine type for variable {}".format(v))
                    position[v] = None

            # Initialise velocity
            velocity = {}
            for v in vars_names:
                var_type = self.search_space.get_variable_type(v)
                if var_type == 'int' or var_type == 'float':
                    lb = self.search_space.get_variable_lbound(v)
                    ub = self.search_space.get_variable_ubound(v)
                    velocity[v] = -abs(ub-lb) + 2*abs(ub-lb)*rand.random()
                elif var_type == 'enumerate':
                    values = self.search_space.get_variable_values(v)
                    velocity[v] = -(len(values)-1) + 2*(len(values)-1)*rand.random()
                elif var_type == 'binary':
                    velocity[v] = -1 + 2*rand.randint(2)
                else:
                    print("Could not determine type for variable {}".format(v))
                    velocity[v] = None
            self.insert_particle(f_bound, position, velocity, seed=seed)
        return 0

    def update_position(self, f_bound, seed=None):
        vars_names = self.search_space.get_variables_names()
        for i in range(self.size):
            new_position = {}
            position = self.particle_list[i].get_position()
            velocity = self.particle_list[i].get_velocity()
            # Get new position
            for v in vars_names:
                var_type = self.search_space.get_variable_type(v)
                if var_type == 'int' or var_type == 'float':
                    new_position[v] = position[v] + velocity[v]
                elif var_type == 'enumerate':
                    new_position[v] = int(position[v] + velocity[v])
                elif var_type == 'binary':
                    new_position[v] = int(position[v] + velocity[v])
            # Force bounds
            if f_bound:
                pos = eval(f_bound)(self.search_space, new_position, seed=seed)
            else:
                pos = new_position
            # Update position
            self.particle_list[i].update_position(pos)
        return 0

    def update_velocity(self, c_inertia, c_local, c_global, seed=None):
        rand.seed(a=seed)
        vars_names = self.search_space.get_variables_names()
        for i in range(self.size):
            new_velocity = {}
            velocity = self.particle_list[i].get_velocity()
            p = self.particle_list[i].get_position()
            p_best_particle = self.particle_list[i].get_particle_best_position()
            p_best_swarm = self.particle_list[i].get_swarm_best_position()
            for v in vars_names:
                new_velocity[v] = c_inertia*velocity[v] + c_local*rand.random()*(p_best_particle[v] - p[v]) + c_global*rand.random()*(p_best_swarm[v] - p[v])
            self.particle_list[i].update_velocity(new_velocity)
        return 0

    def sorted_by_particle_fitness(self, reverse=False):
        particle_list_sorted = []
        tuple_list = []
        for i in range(self.size):
            t = (i, self.particle_list[i].get_fitness())
            tuple_list.append(t)
        tuple_list.sort(key=lambda tup: tup[1], reverse=reverse)
        for t in tuple_list:
            particle_list_sorted.append(self.particle_list[t[0]])
        return particle_list_sorted

    def insert_particle(self, f_bound, position, velocity, seed=None):
        if f_bound:
            pos = eval(f_bound)(self.search_space, position, seed=seed)
        else:
            pos = position
        p = Particle(self.size+1, pos, velocity)
        self.particle_list.append(p)
        self.size += 1
        return 0

    def evaluate(self, f_model, opt_type, synchronous=True):
        self.N_failed_evals = 0
        # Get fitness for all particles
        for i in range(len(self.particle_list)):
            old_fitness = self.particle_list[i].get_fitness()
            fitness = eval(f_model)(self.particle_list[i].get_position())
            self.N_evals += 1
            if fitness:
                # Update particle fitness
                self.particle_list[i].update_fitness(fitness)
                # Update particle and swarm best positions
                if opt_type == 'min':
                    if old_fitness and (fitness < old_fitness):
                        # Update particle best position
                        position = self.particle_list[i].get_position()
                        self.particle_list[i].update_particle_best_position(position)
                        # Update swarm best position
                        if fitness < self.best_particle_current.get_fitness() and synchronous:
                            self.particle_list[i].update_swarm_best_position(position)
                            self.best_particle_current = self.particle_list[i].copy()
                        # Update all time best particle
                        if fitness < self.best_particle_so_far.get_fitness():
                            self.best_particle_so_far = self.particle_list[i].copy()
                if opt_type == 'max':
                    if old_fitness and (fitness > old_fitness):
                        # Update particle best position
                        position = self.particle_list[i].get_position()
                        self.particle_list[i].update_particle_best_position(position)
                        # Update swarm best position
                        if fitness > self.best_particle_current.get_fitness() and synchronous:
                            self.particle_list[i].update_swarm_best_position(position)
                            self.best_particle_current = self.particle_list[i].copy()
                        # Update all time best particle
                        if fitness > self.best_particle_so_far.get_fitness():
                            self.best_particle_so_far = self.particle_list[i].copy()
            else:
                self.N_failed_evals += 1

        # if assynchronous then best swarm position is only updated after determining fitness for all particles
        if not synchronous:
            try:
                if opt_type == 'min':
                    reverse = False
                else:
                    reverse = True
                best_swarm_particle = self.sorted_by_particle_fitness(reverse=reverse)[0]
                best_swarm_position = best_swarm_particle.get_position()
                # Update best particles
                self.best_particle_current = best_swarm_particle
                if self.best_particle_so_far:
                    if opt_type == 'min' and fitness < self.best_particle_so_far.get_fitness():
                        self.best_particle_so_far = best_swarm_particle
                    if opt_type == 'max' and fitness > self.best_particle_so_far.get_fitness():
                        self.best_particle_so_far = best_swarm_particle
                else:
                    self.best_particle_so_far = best_swarm_particle
                # Update all particles
                for i in range(len(self.particle_list)):
                    self.particle_list[i].update_swarm_best_position(best_swarm_position)
            except:
                "Could not update best swarm position in assynchronous mode."

        return [self.N_evals, self.N_failed_evals]


class pso(object):
    """ Creates a real-coded genetic algorithm """
    def __init__(self, search_space, params):
        self.N_iter = 0
        self.params = params
        self.search_space = Search_space(search_space)
        self.seed = params['seed']
        self.swarm_size = params['swarm_size']
        self.max_iter = params['max_iterations']
        self.model_function = params['model_function']
        self.best_particle = None
        self.N_evals = 0
        self.N_failed_evals = 0
        self.statistics = {}
        self.write = {}
        self.synchronous = params['synchronous']
        self.opt_type = params['opt_type']
        if self.opt_type == 'min':
            self.reverse = False
        else:
            self.reverse = True

    def __create_output_dir(self):
        """
        Internal function that creates the output dir and copies the template file
        """
        # Create results directory and create output file from template
        dir_name = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
        output_dir = lib_directory_ops.create_dir(self.params['Excel output dir'], dir_name)
        assert output_dir != None
        new_file = 'output_' + dir_name + '.xlsx'
        output_file = lib_path_ops.join_paths(output_dir, new_file)
        r = lib_file_ops.copy_file(self.params['Excel template file'], output_file)
        self.params['Excel output file'] = output_file
        self.write['generation row index'] = 13
        assert r != None

    def __write_parameters(self):
        """
        Internal function that writes the parameters
        """
        ws = self.wb["Parameters"]
        # Write parameters
        row_i = 4
        for param in self.params.keys():
            ws.cell(row=row_i, column=1, value=param)
            if type(self.params[param]) == type({}):
                ws.cell(row=row_i, column=2, value=str(self.params[param]))
            else:
                ws.cell(row=row_i, column=2, value=self.params[param])
            row_i += 1
        return 0

    def __write_optimal_point(self):
        """
        Internal function that writes the optimal point
        """
        ws = self.wb["Optimisation"]
        if self.params['write_to_console']:
            print("\nOptimal point:")
        # Write optimal point
        col_i = 2
        for v in self.search_space.get_variables_names():
            ws.cell(row=5, column=col_i, value=v)
            ws.cell(row=6, column=col_i, value=self.best_ind.get_solution()[v])
            if self.params['write_to_console']:
                s = '{}: {}'.format(v, self.best_ind.get_solution()[v])
                print(s)
            col_i += 1
        return 0

    def __write_iteration(self):
        """
        Internal function that writes the generation results
        """
        ws = self.wb["Optimisation"]
        # Write variables names
        col_i = 3
        for v in self.search_space.get_variables_names():
            ws.cell(row=12, column=col_i, value=v)
            col_i += 1
        # Write generation info
        row_i = self.write['generation row index']
        ws.cell(row=row_i, column=1, value=self.N_gen)
        ws.cell(row=row_i, column=2, value=self.best_ind.get_fitness())
        col_i = 3
        for v in self.search_space.get_variables_names():
            ws.cell(row=row_i, column=col_i, value=self.best_ind.get_solution()[v])
            col_i += 1
        self.write['generation row index'] += 1

        # Write to console
        if self.params['write_to_console']:
            s = "\t{}\t{}".format(self.N_gen, self.best_ind.get_fitness())
            print(s)
        return 0

    def __write_statistics(self):
        """
        Internal function that writes the statistics
        """
        ws = self.wb["Statistics"]
        # Write statistics
        ws.cell(row=3, column=2, value=self.statistics['N_failed_evals'])
        ws.cell(row=4, column=2, value=self.statistics['N_evals'])
        return 0

    def execute(self):
        """
        Main function of the class, as it runs the pso algorithm.
        """

        # Get functions
        f_model = 'models.' + self.params['model_function']
        if self.params['enforce_bounds']:
            f_bound = 'pso_bound.' + self.params['enforce_bounds_function']
        else:
            f_bound = None

        # Get constants
        c_inertia = self.params['inertia_weight']
        c_local = self.params['acceleration_constant_local']
        c_global = self.params['acceleration_constant_global']

        # Initialise and evaluate population
        swarm = Swarm(self.search_space, self.params)
        swarm.initialise(self.swarm_size, f_bound, seed=self.seed)
        N_evals, N_failed_evals = swarm.evaluate(f_model, self.opt_type, synchronous=False) # False to make sure all particles are correctly initialized
        self.best_particle = swarm.get_best_particle_current()

        # Statistics
        self.statistics['N_evals'] = N_evals
        self.statistics['N_failed_evals'] = N_failed_evals

        # Create output directory and files
#        self.__create_output_dir()
#        self.wb = lib_excel.open_workbook(self.params['Excel output file'])

        # Write initial results
#        if self.params['write_to_console']:
#            print("\nIter.\tFitness")
#        self.__write_parameters()
#        self.__write_iteration()

        # Determine next generation
        while self.N_iter < self.max_iter:
            # Update velocity
            swarm.update_velocity(c_inertia, c_local, c_global, seed=self.seed)

            # Update position
            swarm.update_position(f_bound, seed=self.seed)

            # Evaluate swarm
            N_evals, N_failed_evals = swarm.evaluate(f_model, self.opt_type, synchronous=self.synchronous)
            self.best_particle = swarm.get_best_particle_current()

            # Increment generation
            self.N_iter += 1
            print(self.best_particle.get_fitness())

            # Statistics
            self.statistics['N_evals'] += N_evals
            self.statistics['N_failed_evals'] += N_failed_evals

            # Write results
#            self.__write_iteration()

        # Write optimal results and statistics
#        self.__write_optimal_point()
#        self.__write_statistics()

        # Close necessary files
#        lib_excel.save_workbook(self.wb, self.params['Excel output file'])
#        self.wb.close()

        return self.best_particle

#----------------------------------------------------------------------------------------
# TESTING
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass
