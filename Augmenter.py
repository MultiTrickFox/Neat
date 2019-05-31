from Topology import *
from Gym import *


hm_initial = 20
hm_offspring_per = 2
hm_fittest = 40

hm_iteration = 100


population = tuple(Topology() for _ in range(hm_initial))

for _ in range(hm_iteration):

    # todo : mutate & crossover & fittests

    pass
    # for topology in population:
    #     population.append(mutate_add_connection(topology.copy()))
    #     population.append(mutate_split_connection(topology.copy()))
    #     population.append(mutate_alter_connection(topology.copy()))





