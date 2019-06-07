from sklearn.manifold import TSNE

from random import choice, random
from numpy.random import randn

from numpy import array

from copy import copy


debug = False


# params

hm_ins  = 2
hm_outs = 1

prob_crossover      = 0.5
prob_mutate_add     = 0.3
prob_mutate_split   = 0.4
prob_mutate_alter   = 0.2
prob_mutate_express = 0.2


# globals

innovation_ctr = 0
hidden_ctr = 0

connections_unique = []


# structs

class Node:
    def __init__(self, hidden_id, type):
        self.type = type
        self.id = hidden_id

        # graph builder variables ; reminder : if used, immediately =[] & =0 after the operation.
        self.outgoings = []
        self.value = 0

    def __str__(self):
        return self.type + str(self.id)


class Connection:
    def __init__(self, innovation_id, from_node, to_node, weight, is_expressed):
        self.innovation_id = innovation_id
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
        self.is_expressed = is_expressed

    def __copy__(self):
        return Connection(self.innovation_id, self.from_node, self.to_node, self.weight, self.is_expressed)

    def __eq__(self, other):
        return (self.from_node == other.from_node) and (self.to_node == other.to_node)


class Topology:
    def __init__(self, nodes=None, connections=None):
        self.nodes = nodes if nodes else in_nodes + out_nodes
        self.connections = connections if connections else []

    def __copy__(self):
        return Topology(self.nodes, [copy(connection) for connection in self.connections])

    def __call__(self, in_vector):

        # initialize graph

        for connection in self.connections:
            connection.from_node.outgoings.append((connection.to_node, connection.weight))

        for node in self.nodes:
            node.value = 0

        input_nodes = self.nodes[:hm_ins]
        out_nodes = self.nodes[hm_ins:hm_ins+hm_outs]

        # process graph

        for input, input_node in zip(in_vector, input_nodes):
            for child, weight in input_node.outgoings:
                self.forward(child, input * weight)

        # collect outputs

        outputs = [out_node.value for out_node in out_nodes]

        # release graph

        for node in self.nodes:
            node.outgoings = []
            node.value = 0

        return outputs

    def forward(self, node, incoming):
        node.value += incoming
        for child, weight in node.outgoings:
            self.forward(child, incoming * weight)


# helpers


tsne = TSNE(n_iter=250, n_components=2)

in_nodes = [Node(_, "in") for _ in range(hm_ins)]
out_nodes = [Node(_, "out") for _ in range(hm_outs)]


def topology_difference(topology1, topology2, k1=1, k2=1, k3=0.4):

    if topology1.connections and topology2.connections:

        # initialize variables

        hm_connections1, hm_connections2 = len(topology1.connections), len(topology2.connections)
        hm_connections = max(hm_connections1, hm_connections2)

        innovations1 = [connection.innovation_id for connection in topology2.connections]
        max_innovation1, min_innovation1 = max(innovations1), min(innovations1)

        hm_excess_connections = 0
        hm_disjoint_connections = 0
        avg_weight_difference = 0

        # count up details

        for connection1 in topology1.connections:
            for connection2 in topology2.connections:

                if (connection1.from_node != connection2.from_node) and \
                        (connection1.to_node != connection2.to_node):
                    if min_innovation1 < connection2.innovation_id < max_innovation1:
                        hm_disjoint_connections += 1
                    else:
                        hm_excess_connections += 1

                avg_weight_difference += abs(connection1.weight-connection2.weight)

        avg_weight_difference /= hm_connections1*hm_connections2

        # apply formula

        return k1*hm_excess_connections/hm_connections + k2*hm_disjoint_connections/hm_connections + k3*avg_weight_difference

    else:

        return 1


def divide_into_species(population):

    species = [[], [], [], []]

    # calculate differences

    # differences = []
    #
    # for i, t1 in enumerate(population):
    #     differences.append([])
    #     for t2 in population[i+1:]:
    #         differences[-1].append(topology_difference(t1, t2))
    #
    # diffs = [e1 for e2 in differences for e1 in e2]
    # avg_difference = sum(diffs) / len(diffs)

    # similar topologies wrt each topology

    # similars = [[t2 for i2, t2 in enumerate(population[i1+1:])
    #                 if differences[i1][i2] < avg_difference]
    #                     for i1, t1 in enumerate(population)]

    # tsne

    # innovations = [[conn.innovation_id for conn in topology.connections] for topology in population]
    # tsne_input = [[1 if _ in innovations[i] else 0 for _ in range(innovation_ctr if innovation_ctr !=0 else 1)] for i,topology in enumerate(population)]
    
    tsne_input = [[topology_difference(t1,t2) if t1 != t2 else 0 for t1 in population] for t2 in population]

    tsne_output = tsne.fit_transform(array(tsne_input))
    xs, ys = tsne_output[:, 0], tsne_output[:, 1]
    locations = tuple((x,y) for x,y in zip(xs,ys))

    min_x, max_x = min(tsne_output[:, 0]), max(tsne_output[:, 0])
    min_y, max_y = min(tsne_output[:, 1]), max(tsne_output[:, 1])

    mid_x, mid_y = (min_x+max_x)/2, (min_y+max_y)/2

    for i, topology in enumerate(population):
        x,y = locations[i]

        if x < mid_x:
            if y < mid_y:
                species[0].append(topology)

            else:
                species[1].append(topology)
        else:
            if y < mid_y:
                species[2].append(topology)

            else:
                species[3].append(topology)


    # species = [[], []]
    #
    # sentinel = 0  # all elements are checked wrt. population[0]
    #
    # differences = [[topology_difference(t1, t2) if t1 != t2 else None
    #                 for t2 in population]
    #                for t1 in population]
    #
    # avg_difference = sum([e for diff in differences for e in diff if e is not None]) / (
    #             len(population) * (len(population) - 1))
    #
    # for i,topology in enumerate(population):
    #     diffs = differences[i]
    #     if diffs[sentinel] is not None:
    #
    #         if diffs[sentinel] <= avg_difference:
    #             species[0].append(topology)
    #         elif avg_difference < diffs[sentinel]:
    #             species[1].append(topology)

    if debug: print(f'species: {len(species[0])} - {len(species[1])}')

    return species


def is_reachable(node_from, node_to):

    if node_from.type == "hidden" and node_to.type == "hidden":

        if node_from == node_to: return True

        # build graph

        node_from.outgoings = [connection.to_node for connection in connections_unique if connection.from_node == node_from]

        # process

        if not node_from.outgoings:

            is_it = False

        else:

            if node_to in node_from.outgoings:

                is_it = True

            else:

                # print(len(node_from.outgoings))

                is_it = any([is_reachable(node, node_to) for node in node_from.outgoings])

        # release graph

        node_from.outgoings = []

        return is_it

    else:

        return False


def pick_nodes_to_connect(genome):

    node_from = choice(genome.nodes)
    node_to = choice(genome.nodes)

    # check for self-connections

    while (node_from.type == "in" and node_to.type == "in") \
            or \
            (node_from.type == "out" and node_to.type == "out"):
        node_from = choice(genome.nodes)
        node_to = choice(genome.nodes)

    # check if connection needs to be reversed

    if (node_from.type == "out" and node_to.type == "hidden") \
            or \
            (node_from.type == "hidden" and node_to.type == "in") \
            or \
            (node_from.type == "out" and node_to.type == "in"):
        node_from, node_to = node_to, node_from

    return node_from, node_to


# mutation operations


def mutate_add_connection(genome):
    if random() < prob_mutate_add:

        global innovation_ctr
        global connections_unique

        # pick nodes to connect

        node_from, node_to = pick_nodes_to_connect(genome)
        i = 0
        while is_reachable(node_to, node_from) and i < 3:
            node_from, node_to = pick_nodes_to_connect(genome)
            i += 1
            if i == 3 and is_reachable(node_to, node_from):
                return

        # check if connection exists in genome

        exists_in_genome = False

        for connection in genome.connections:
            if (node_from == connection.from_node) and \
                    (node_to == connection.to_node):
                        exists_in_genome = True
                        break

        if not exists_in_genome:

            connection = Connection(innovation_ctr, node_from, node_to, randn(), True)

            # check if connection exists in global

            exists_in_global = False

            for connection_unique in connections_unique:
                if (node_from == connection_unique.from_node) \
                        and \
                        (node_to == connection_unique.to_node):

                    exists_in_global = True

                    # update locals

                    connection = copy(connection_unique)
                    node_from = connection.from_node
                    node_to = connection.to_node

                    break

            if not exists_in_global:

                # update globals

                connections_unique.append(copy(connection))
                innovation_ctr += 1

            else:

                # update genome

                if node_from not in genome.nodes:
                    genome.nodes.append(node_from)
                if node_to not in genome.nodes:
                    genome.nodes.append(node_to)

            # create connection

            if debug: print(f'creating connection {connection.from_node} -> {connection.to_node}')

            genome.connections.append(connection)

            return genome

        else:

            connection.is_expressed = True


def mutate_split_connection(genome, connection=None):
    if len(genome.connections) > 0 and random() < prob_mutate_split:

        global innovation_ctr
        global hidden_ctr
        global connections_unique

        if not connection: connection = choice(genome.connections)
        connection.is_expressed = False

        # check if connections exist in genome

        exists_in_genome = False

        connections_from_from_node = [c for c in genome.connections if (c.from_node == connection.from_node) and (c.to_node != connection.to_node)]
        possible_nodes = [c.to_node for c in connections_from_from_node]
        connections_to_to_node = [c for c in genome.connections if (c.to_node == connection.to_node) and (c.from_node in possible_nodes)]

        if connections_to_to_node:

            exists_in_genome = True

        if not exists_in_genome:

            # check if connections exist in global

            exists_in_global = False

            connections_from_from_node = [c for c in connections_unique if (c.from_node == connection.from_node) and (c.to_node != connection.to_node)]
            possible_nodes = [c.to_node for c in connections_from_from_node]
            connections_to_to_node = [c for c in connections_from_from_node if (c.to_node == connection.to_node) and (c.from_node in possible_nodes)]

            if connections_to_to_node:

                exists_in_global = True

                # update locals

                node = connections_to_to_node[-1].from_node
                for c in connections_from_from_node:
                    if c.to_node == node:
                        connection1 = copy(c)
                        break
                connection2 = copy(connections_to_to_node[-1])

            else:

                node = Node(hidden_ctr, "hidden")
                connection1 = Connection(innovation_ctr, connection.from_node, node, 1.0, True)
                innovation_ctr += 1
                connection2 = Connection(innovation_ctr, node, connection.to_node, connection.weight, True)
                innovation_ctr += 1

            if not exists_in_global:

                # update globals

                connections_unique.append(copy(connection1))
                connections_unique.append(copy(connection2))
                hidden_ctr += 1
                # if node not in nodes_unique:
                #     nodes_unique.append(node)

            # update genome

            if node not in genome.nodes:
                genome.nodes.append(node)

            # create connection

            if debug: print(f'splitting connection {connection.from_node} -> {connection.to_node}')

            genome.connections.append(connection1)
            genome.connections.append(connection2)

            return genome


def mutate_alter_connection(genome):

    # change weight

    if len(genome.connections) > 0 and random() < prob_mutate_alter:
        connection = choice(genome.connections)
        connection.weight += randn()

        return genome


def mutate_onoff_connection(genome):

    # enable disable

    if len(genome.connections) > 0 and random() < prob_mutate_express:
        connection = choice(genome.connections)
        connection.is_expressed = not connection.is_expressed

        return genome


# crossover operation


def crossover(genome1, genome2):  # assuming genome1_fitness > genome2_fitness

    if random() < prob_crossover:

        # new nodes are based on parent1

        genome = Topology(genome1.nodes, [])

        # new connections are based on parent1 and parent2

        for connection1 in genome1.connections:

            # check if same connection exists in parent2

            exists_in2 = False
            for connection2 in genome2.connections:
                if connection1.innovation_id == connection2.innovation_id:
                    exists_in2 = True
                    break

            # mating

            connection = copy(connection1)if not exists_in2 else \
                (copy(connection1) if random() < 0.5 else copy(connection2))

            genome.connections.append(connection)

            for e in (connection.from_node, connection.to_node):
                    if e not in genome.nodes:
                        genome.nodes.append(e)

        return genome
