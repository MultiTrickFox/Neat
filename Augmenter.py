from pickle import dump, load
from operator import itemgetter

from Topology import *
from Gym import *


load_model = False


hm_initial = 50
hm_fittest = 20

hm_iteration = 1_000


if not load_model:

    population = [Topology() for _ in range(hm_initial)]

    for _ in range(hm_iteration):

        # TODO block

        # separate into species
        # hm_fittest of each specie
        # breed

        # pass



        # mutate

        muts = []

        for topology in population:

            for mutation in (mutate_add_connection(copy(topology)),
                             mutate_split_connection(copy(topology)),
                             mutate_alter_connection(copy(topology)),
                             mutate_onoff_connection(copy(topology)),
                             ):
                if mutation:
                    muts.append(mutation)

        population.extend(muts)

        # breed

        news = []

        for i, topology1 in enumerate(population):
            for topology2 in population[i+1:]:

                res = crossover(copy(topology1), copy(topology2))
                if res:
                    news.append(res)

        population.extend(news)

        # survive

        species = divide_into_species(population)

        species_results = [sorted({_:play_a_round(t) for _,t in enumerate(population)}.items(), key=itemgetter(1), reverse=True)
                           for population in species]

        # results = sorted({_:play_a_round(t) for _,t in enumerate(population)}.items(), key=itemgetter(1), reverse=True)

        population = [population[e[0]] for specie_result in species_results for e in specie_result[:hm_fittest]]
        scores = [sum([e[1] for e in specie_result[:hm_fittest]]) for specie_result in species_results]

        # print(scores)

        print(f'iteration {_} fitness: {sum(scores)}, {scores}', flush=True)
        # with open(f'iter{_}_fit.pkl','wb+') as f:
        #     dump(population[0], f)
        # with open(f'iter{_}_pop.pkl','wb+') as f:
        #     dump(population, f)

else:

    with open('pop.pkl','rb') as f:
        pop = load(f)

    print('Showing result..')

    play(pop[2])


env.close()
