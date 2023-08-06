# @Author: Felix Kramer <felix>
# @Date:   2022-07-27T15:50:36+02:00
# @Email:  felixuwekramer@proton.me
# @Filename: cycle_sampling.py
# @Last modified by:   felix
# @Last modified time: 2022-07-28T15:16:36+02:00
import networkx as nx
import numpy as np
import numpy.random as nr
import random as rd
import itertools as it
import snarlpy.edge_algebra as edge_algebra


def generate_random_coordinate(nullity):
    """
    Generate a binary sequence vector of length 'nullity'.

    Args:
        nullity (int): \n
            The cyclomatic number determining the length of the binary vector.
    Returns:
        list: \n
            A binary vector for cycle sampling from a set of cardinality
            'nullity'.
    """

    while True:
        k = nr.rand(nullity)
        r = np.round(k, 0)
        if not np.all(r == 0):
            break

    return r.astype(int)


def generate_random_index(nullity):

    """
    Generate an index vector for sampling from a cycle basis of cardinality
    'nullity'.

    Args:
        nullity (int): \n
            The cyclomatic number determining the length of the binary vector.
    Returns:
        list: \n
            An index vector for cycle sampling from a set of cardinality
            'nullity'.
    """
    k = generate_random_coordinate(nullity)
    idx = [i for i in range(nullity) if k[i] == 1]

    return idx.astype(int)


def get_keyNumbers_forBinary(null, iteration):

    """
    Sample a random index from the cycle space of a graph with nullity 'null'.
    Args:
        null (int): \n
            The cyclomatic number determining the the exponential size of
            the cycle space.
        iteration (int): \n
            Sample size.
    Returns:
        iterable: \n
            An index vector for cycle sampling from a set of basis cardinality
            'null'.
    """
    exp = (2**null)-1
    rnd_num = it.product(
        [rd.randint(1, exp) for i in range(iteration)], [null]
        )

    return rnd_num


def grab_cycles_from_space(*args):
    """
    Generate random cycle space coefficient vectors.

    Args:
        args (list): \n
            A list of cyclomatic numbers.
    Returns:
        iterable: \n
            A list of binary vectors for further cycle sampling processes.
    """
    coeff = [generate_random_coordinate(a) for a in args]

    return coeff


def grab_all_cycles_from_space(*args):
    """
    Generate and catch all cycle space coefficient vectors.
    (CAREFUL CYCLE SPACES HAVE EXPONENTIAL COMPLEXITY, ONLY USE FOR SMALL
    CYCLOMATIC NUMBERS)

    Args:
        args (list): \n
            A list of cyclomatic numbers.
    Returns:
        iterable: \n
            A list of binary vectors for further cycle sampling processes.
    """
    aux = []

    for i, a in enumerate(args):

        exp = 2**a
        tmp = [get_binary(j, a) for j in range(1, exp)]

        aux.append(tmp[:])

    if len(args) > 1:
        total_key_set = it.product(*aux)
    else:
        total_key_set = aux[0]

    return list(total_key_set)


def get_binary(j, a):
    """
    Generate a binary sequence vector of length a.

    Args:
        j (int): \n
            The j-th binary to generate.
        a (int): \n
            The cyclomatic number deterining the vector length/scope.
    Returns:
        list: \n
            A binary vector for further cycle sampling processes.
    """
    # binNumb=format(j,'#0'+str(a)+'b')
    # binNumb = binNumb[2:]
    binNumb = f'{j:0{a}b}'
    seq = [int(b) for b in binNumb]

    return seq


def generate_networkx_cycle_from_edges(edge_set, input_graph):
    """
    Generate networkx.Graph object representing a basis cycle from a given
    edge subset.

    Args:
        edge_set (list): \n
            The binary edge vector representing the cycle.
        input_graph (networkx.Graph): \n
            The original simple graph used for reduction.
    Returns:
        networkx.Graph: \n
            A simple eulerian cycle.
    """
    nx_cycle = nx.Graph()
    edge_bunch = [
        e for i, e in enumerate(input_graph.edges()) if edge_set[i] == 1
        ]
    nx_cycle.add_edges_from(edge_bunch)

    return nx_cycle


def get_new_cycle(new_key, cycle_matrix, backbone_graph):
    """
    Generate a new networkx.Graph object, representing a cycle from a given
    graph, its cycle basis and a binary coefficient vector.

    Args:
        new_key (int): \n
            The binary coefficient vectorto generate a cycle superpostion.
        cycle_matrix (int): \n
            The graph's mesh matrix for a given cycle basis.
        backbone_graph (int): \n
            The input graph used to reconstruct a full networkx.Graph object

    Returns:
        networkx.Graph: \n
            A simple eulerian cycle.
    """
    new_edges = edge_algebra.get_cycle_superpositions_edge_vector(
        new_key, cycle_matrix
        )
    new_cycle = generate_networkx_cycle_from_edges(new_edges, backbone_graph)

    return new_cycle


def get_new_cycle_components(edge_set, edge_matrix, nx_cycle, backbone_graph):
    """
    Generate a new networkx.Graph object, representing a cycle from a given
    graph, its cycle basis and a binary coefficient vector.

    Args:
        edge_set (list): \n
            A list of all edges in the simple graph.
        edge_matrix (list): \n
            The binary mesh matrix of the graph.
        nx_cycle (networkx.Graph): \n
            The networx.Graph object representing a Eulerian cycle.
        backbone_graph (networkx.Graph): \n
            The original simple graph used for reduction.

    Returns:
        ndarray: \n
            The coefficient vector for given cycle in the current
            cycle basis.
        networkx.Graph: \n
            The rebuild of the given Eulerian cycle for simplification.
    """
    es = edge_algebra.edge_column_binary(nx_cycle, edge_set)
    new_key = edge_algebra.get_component_key(es, edge_matrix)

    new_cycle = get_new_cycle(new_key, edge_matrix, backbone_graph)

    return new_key, new_cycle


def get_new_cycle_components_gamma(edge_set, edge_matrix, key, backbone_graph):
    """
    Generate a new networkx.Graph object, representing a cycle from a given
    graph, its cycle basis and a binary coefficient vector.

    Args:
        edge_set (list): \n
            A list of all edges in the simple graph.
        edge_matrix (list): \n
            The binary mesh matrix of the graph.
        key (networkx.Graph): \n
            An index list indicating which cycles are to be superimposed.
        backbone_graph (networkx.Graph): \n
            The original simple graph used for reduction.

    Returns:
        ndarray: \n
            The coefficient vector for given cycle in the current
            cycle basis.
        networkx.Graph: \n
            The rebuild of the given Eulerian cycle for simplification.
    """

    new_edges = edge_algebra.get_cycle_superpositions_edge_vector(
        key, edge_matrix
        )

    new_key = edge_algebra.get_component_key(new_edges, edge_matrix)

    new_cycle = get_new_cycle(new_key, edge_matrix, backbone_graph)

    return new_key, new_cycle
