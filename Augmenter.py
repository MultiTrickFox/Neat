from operator import itemgetter
import Topology ; Topology.debug = False

from Topology import *
from Gym import *


hm_initial = 20
hm_offspring_per = 2
hm_fittest = 40

hm_iteration = 100


population = [Topology() for _ in range(hm_initial)]

for _ in range(hm_iteration):

    # mutate

    muts = []

    for topology in population:

        for mutation in (mutate_add_connection(topology.copy()),
                         mutate_split_connection(topology.copy()),
                         mutate_alter_connection(topology.copy()),
                         mutate_onoff_connection(topology.copy())):
            if mutation:
                muts.append(mutation)

    population.extend(muts)

    # breed

    news = []

    for topology in population:

        res = crossover(topology, choice(population))
        if res:
            news.append(res)

    population.extend(news)

    # survive

    results = sorted({_:play_a_round(topology) for _,t in enumerate(population)}.items(), key=itemgetter(1))

    population = [population[e[0]] for e in results[:hm_fittest]]
    scores = [e[1] for e in results[:hm_fittest]]

    sum_score = sum(scores) / len(population)
    print(f'iteration {_} overall score: {sum_score}')
