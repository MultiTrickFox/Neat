from random import choice, random
from numpy.random import randn


debug = True


# params

hm_ins = 2
hm_outs = 2

prob_mutate_add = 1
prob_mutate_split = 1
prob_mutate_alter = 1
prob_mutate_express = 1
prob_crossover = 1


# globals

innovation_ctr = 0

connections_unique = []
nodes_unique = []


# structs

class Node:
    def __init__(self, node_type):
        self.type = node_type


class Connection:
    def __init__(self, innovation_id, from_node, to_node, weight, is_expressed):
        self.innovation_id = innovation_id
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
        self.is_expressed = is_expressed

    def copy(self):
        return Connection(self.innovation_id, self.from_node, self.to_node, self.weight, self.is_expressed)


class Topology:
    def __init__(self, nodes=None, connections=None):
        if not nodes:
            nodes = in_nodes + out_nodes
        if not connections:
            connections = []
        self.nodes = nodes
        self.connections = connections

    def copy(self):
        return Topology(self.nodes, self.connections)

    def __call__(self):
        outs = [0.0 for _ in range(hm_outs)]



# helpers


in_nodes = [Node("in") for _ in range(hm_ins)]
out_nodes = [Node("out") for _ in range(hm_outs)]

# nodes_unique.extend(in_nodes)
# nodes_unique.extend(out_nodes)


# mutation operations


def mutate_add_connection(genome):
    if random() < prob_mutate_add:

        global innovation_ctr
        global connections_unique

        node_from = choice(genome.nodes)
        node_to = choice(genome.nodes)

        # check for self-connections input & output

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

                    connection = connection_unique.copy()
                    node_from = connection.from_node
                    node_to = connection.to_node

                    break

            if not exists_in_global:

                # update globals

                connections_unique.append(connection.copy())
                innovation_ctr += 1
                # if node_to not in nodes_unique:
                #     nodes_unique.append(node_to)
                # if node_from not in nodes_unique:
                #     nodes_unique.append(node_from)

            else:

                # update genome

                if node_from not in genome.nodes:
                    genome.nodes.append(node_from)
                if node_to not in genome.nodes:
                    genome.nodes.append(node_to)

            # create connection

            if debug: print(f'creating connection {connection.from_node.type} -> {connection.to_node.type}')

            genome.connections.append(connection)


def mutate_split_connection(genome, connection=None):
    if len(genome.connections) > 0 and random() < prob_mutate_split:

        global innovation_ctr
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
                        connection1 = c.copy()
                        break
                connection2 = connections_to_to_node[-1].copy()

            else:

                node = Node("hidden")
                connection1 = Connection(innovation_ctr, connection.from_node, node, 1.0, True)
                innovation_ctr += 1
                connection2 = Connection(innovation_ctr, node, connection.to_node, connection.weight, True)
                innovation_ctr += 1

            if not exists_in_global:

                # update globals

                connections_unique.append(connection1.copy())
                connections_unique.append(connection2.copy())
                # if node not in nodes_unique:
                #     nodes_unique.append(node)

            # update genome

            if node not in genome.nodes:
                genome.nodes.append(node)

            # create connection

            if debug: print(f'splitting connection {connection.from_node.type} -> {connection.to_node.type}')

            genome.connections.append(connection1)
            genome.connections.append(connection2)


def mutate_alter_connection(genome):

    # change weight

    if len(genome.connections) > 0 and random() < prob_mutate_alter:
        connection = choice(genome.connections)
        connection.weight += randn()


def mutate_onoff_connection(genome):

    # enable disable

    if len(genome.connections) > 0 and random() < prob_mutate_express:
        connection = choice(genome.connections)
        connection.is_expressed = not connection.is_expressed


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

            connection = connection1.copy() if not exists_in2 else \
                (connection1.copy() if random() < 0.5 else connection2.copy())

            genome.connections.append(connection)

            for e in (connection.from_node, connection.to_node):
                    if e not in genome.nodes:
                        genome.nodes.append(e)

        return genome
