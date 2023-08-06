# @Author: Felix Kramer <felix>
# @Date:   2022-07-27T15:50:36+02:00
# @Email:  felixuwekramer@proton.me
# @Filename: signature.py
# @Last modified by:   felix
# @Last modified time: 2022-07-28T18:12:09+02:00
import networkx as nx
import random as rd


def extract_eulerpath(nx_cycle, root):
    """
    Extract the Eulerian path as an edge sequence from a cycle, given an
    arbitrary starting node.

    Args:
        nx_cycle (networkx.Graph): \n
            A networkx.Graph object represeting a cycle.
        nroot (networkx.Graph.node): \n
            A networkx.Graph.node object to start the path search.
    Returns:
        iterable: \n
            A sequence of edges (ordered)/ a walk along the cyle.
    """

    ep = nx.eulerian_path(nx_cycle, source=root)

    return ep


def get_signature(nx_cycle, sig_graph):
    """
    Given a simple graph for reference, compute the edge signatures for the
    Eulerian path through the cycle.

    Args:
        nx_cycle (networkx.Graph): \n
            A networkx.Graph object represeting a cycle.
        sig_grapht (dict): \n
            A dictionary holding the signature information for any edge in the
            reference graph.
    Returns:
        dict: \n
            A dictionary holding the signature information for any edge in the
            cycle graph.
    """

    sig_cycle = {}

    list_e = list(extract_eulerpath(nx_cycle, list(nx_cycle.nodes())[0]))

    for e in list_e:
        sig_cycle[e] = get_relative_direction(e, sig_graph)

    return sig_cycle


def get_signature_rand(nx_cycle, sig_graph):
    """
    Given a simple graph for reference, compute the edge signatures for the
    Eulerian path through the cycle. Randomize the root node during path
    search.

    Args:
        nx_cycle (networkx.Graph): \n
            A networkx.Graph object represeting a cycle.
        sig_grapht (dict): \n
            A dictionary holding the signature information for any edge in the
            reference graph.
    Returns:
        dict: \n
            A dictionary holding the signature information for any edge in the
            cycle graph.
    """
    sig_cycle = {}

    list_e = list(
        extract_eulerpath(nx_cycle, rd.choice(list(nx_cycle.nodes())))
        )

    for e in list_e:
        sig_cycle[e] = get_relative_direction(e, sig_graph)

    return sig_cycle


def get_edge_direction(edge_set):
    """
    Setting the intrinsic direction for all edges in a given set.

    Args:
        edge-set (list): \n
            A set of edges, with aplha and omega nodes non-equal.
    Returns:
        dict: \n
            A dictionary holding the signature information for any edge in the
            set.
    """
    sig = {}
    for j, e in enumerate(edge_set):

        sig[e] = [e[0], e[1]]

    return sig


def get_relative_direction(edge, sig_graph):
    """
    Getting the edge signature for an edge set in relation to a reference set.

    Args:
        edge-set (list): \n
            A set of edges, with aplha and omega nodes non-equal.
        sig_grapht (dict): \n
            A dictionary holding the signature information for any edge in the
            reference graph.
    Returns:
        dict: \n
            A dictionary holding the signature information for any edge in the
            set.
    """
    signature = 0
    if edge in sig_graph.keys():
        signature = 1
    else:
        signature = -1

    return signature
