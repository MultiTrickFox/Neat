from model import *


g = Genome()

mutate_add_connection(g)

# for _ in range(10):
#     mutate_split_connection(g)


gc = Genome()

mutate_add_connection(gc)

g_child = crossover(g, gc)


mutate_split_connection(g_child)

