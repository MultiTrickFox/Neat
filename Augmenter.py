from pickle import dump, load
from operator import itemgetter

from Topology import *
from Gym import *


load_model = True


hm_initial = 50
hm_offspring_per = 2
hm_fittest = 50

hm_iteration = 10


if not load_model:

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

        for mut in muts:
            if mut in population:
                print('wtf error2')


        population.extend(muts)

        # breed

        news = []

        for topology in population:

            res = crossover(topology.copy(), choice(population).copy())
            if res:
                news.append(res)

        population.extend(news)

        # survive

        results = sorted({_:play_a_round(t) for _,t in enumerate(population)}.items(), key=itemgetter(1), reverse=True)

        population = [population[e[0]] for e in results[:hm_fittest]]
        scores = [e[1] for e in results[:hm_fittest]]

        print(scores)

        print(f'iteration {_} fitness: {scores[0]}, {sum(scores) / len(population)}', flush=True)
        with open(f'iter{_}_fit.pkl','wb+') as f:
            dump(population[0], f)
        with open(f'iter{_}_pop.pkl','wb+') as f:
            dump(population, f)

else:

    with open('pop.pkl','rb') as f:
        pop = load(f)

    print('Showing result..')

    play(pop[2])


env.close()
