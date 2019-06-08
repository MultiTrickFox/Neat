from pickle import dump, load
from operator import itemgetter

from Topology import *
from Gym import *


def main():

    display_model = False

    load_model = False
    single_specie = True


    hm_initial = 5000
    hm_fittest = 500

    hm_iteration = 50


    if not display_model:

        population = [Topology() for _ in range(hm_initial)] if not load_model else load(open('pop.pkl', 'rb'))

        for _ in range(hm_iteration):

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

            # specify

            if not single_specie:
                species = divide_into_species(population)
            else:
                species = [population, [], [], []]

            # survive

            species_results = [
                sorted({_: play_a_round(t) for _, t in enumerate(population)}.items(), key=itemgetter(1), reverse=True)
                for population in species]

            species = [[specie[e[0]] for e in specie_result[:hm_fittest]]
                       for specie,specie_result in zip(species, species_results)]

            population = species[0] + species[1] + species[2] + species[3]

            scores = [specie_result[0][1] for specie_result in species_results if specie_result]

            # breed

            for specie in species:

                news = []

                for i, topology1 in enumerate(specie):
                    for topology2 in specie[i + 1:hm_fittest]:

                        res = crossover(copy(topology1), copy(topology2))
                        if res:
                            news.append(res)

                specie.extend(news)

            # survive

            species_results = [
                sorted({_: play_a_round(t) for _, t in enumerate(population)}.items(), key=itemgetter(1), reverse=True)
                for population in species]

            species = [[specie[e[0]] for e in specie_result[:hm_fittest]]
                       for specie, specie_result in zip(species, species_results)]

            population = species[0] + species[1] + species[2] + species[3]

            scores = [specie_result[0][1] for specie_result in species_results if specie_result]

            print(f'iteration {_} ; max: {max(scores)} ; fitness: {scores} ; populations: {[len(pop) for pop in species]}', flush=True)

            # breed again

            population_breed = [population[e[0]] for e in sorted({_: play_a_round(t) for _, t in enumerate(population)}.items(), key=itemgetter(1), reverse=True)[:hm_fittest]]

            for i, topology1 in enumerate(population_breed):
                for topology2 in population_breed[i + 1:hm_fittest]:

                    res = crossover(copy(topology1), copy(topology2))
                    if res:
                        population.append(res)

    # displaying results

        # save

        pop_sort = sorted({_: play_a_round(t) for _, t in enumerate(population)}.items(), key=itemgetter(1), reverse=True)
        print(pop_sort)  # TODO : remove
        fittest = population[pop_sort[0][0]]
        print(f'fittest: {pop_sort[0][1]}, sickest: {pop_sort[-1][1]}')

        with open(f'fit.pkl', 'wb+') as f:
            dump(fittest, f)
        with open(f'pop.pkl', 'wb+') as f:
            dump(population, f)

            # display

            play(fittest)


    else:

        # with open('fit.pkl', 'rb') as f:
        #     fit = load(f)
        with open('pop.pkl', 'rb') as f:
            population = load(f)
            pop_sort = sorted({_: play_a_round(t) for _, t in enumerate(population)}.items(), key=itemgetter(1),
                              reverse=True)
            fit = population[pop_sort[0][0]]

        print('Showing result..')

        play(fit)

    # cleanup

    env.close()


if __name__ == '__main__':
    main()