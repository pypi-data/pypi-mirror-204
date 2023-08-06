# @Author:  Felix Kramer
# @Date:   2021-09-25T14:20:58+02:00
# @Email:  kramer@mpi-cbg.de
# @Project: go-with-the-flow
# @Last modified by:   felix
# @Last modified time: 2022-07-28T18:45:01+02:00
# @License: MIT
import networkx as nx
import numpy as np

import snarlpy.edge_algebra as edge_algebra
import snarlpy.signature as signature
import snarlpy.cycleToolsLinking as ctl


def calc_nullity(G):

    """
    Compute a simple graph's nullity/cyclomatic number.

    Args:
        G (networkx.Graph):\n
            A simple graph.

    Returns:
        int:\n
            The cyclomatic number of the graph.

    """

    E = nx.number_of_edges(G)
    N = nx.number_of_nodes(G)
    CC = nx.number_connected_components(G)
    nullity = E-N+CC

    return nullity


def calc_basisIntertwinedness(graph_sets):
    """
    Compute the first intertwinedness metrics (linkage matrices for arbitrary
    cycle bases).

    Args:
        grap_sets (list):\n
            A list of networkx.Graph objects which posses a defined spatial
            embedding (nodal pos-attributes).

    Returns:
        list:\n
            A list of the arbitrarily chosen cycle matrix for the graphs.
        ndarray:\n
            The linkage matrix of the graph set.

    """

    # generate basis vectors and corresponding graph matrices
    # cyc_nx_bases=[calc_cycle_basis(G) for G in graph_sets]
    cyc_nx_bases = [calc_cycle_minimum_basis(G) for G in graph_sets]

    # compute linkage of basis vectors
    numeric_res = calc_basis_linkage(*cyc_nx_bases)
    lk_mat = extract_linkage_matrix(numeric_res)

    return cyc_nx_bases, lk_mat


def get_basis_matrices(input_graphs, cyc_nx_base):
    """
    Compute auxillary matrix sets for further computation intertwinedness
    metrics.

    Args:
        input_graphs (list):\n
            A list of networkx.Graph objects which posses a defined spatial
            embedding (nodal pos-attributes).
        cyc_nx_base (list):\n
            A list of basis cycles for each graph.

    Returns:
        list:\n
            A list of edge-tuples for each graph.
        list:\n
            The respective edge signatures for each graph.
        list:\n
            A list of (directed) mesh matrices for each graph.
        list:\n
            A list of (undirected) mesh matrices for each graph.

    """
    # get edge representations of graphs
    edge_mat = [list(G.edges()) for G in input_graphs]

    sig = [signature.get_edge_direction(e) for e in edge_mat]

    # init cycle matrices directed and undirected, note they are transposed to
    # each other
    set_size = len(input_graphs)

    cyc_mat_dir = [
        edge_algebra.generate_edge_matrix(
            cyc_nx_base[i], edge_mat[i], sig[i]) for i in range(set_size)
        ]

    cyc_mat_undir = [
        edge_algebra.generate_edge_matrix_binary(
            cyc_nx_base[i], edge_mat[i]) for i in range(set_size)
        ]

    return edge_mat, sig, cyc_mat_dir, cyc_mat_undir


def calc_cycle_basis(nx_graph):
    """
    Compute a cycle basis of a simple graph via a bfs search algorithm.

    Args:
        nx_graph (networkx.Graph):\n
            A simple graph.

    Returns:
        list:\n
            A list of networkx.Graph objeccts, represting the basis cycles of
            the input graph.

    """
    S = ctl.linkedCycles_tools()
    S.G = nx.Graph(nx_graph)
    basis_nx = S.construct_networkx_basis()

    return basis_nx


def calc_cycle_minimum_basis(nx_graph):
    """
    Compute a minimal topological cycle basis of a simple graph via Horton's
    algorithm.

    Args:
        nx_graph (networkx.Graph):\n
            A simple graph.

    Returns:
        list:\n
            A list of networkx.Graph objects, represting the basis cycles of
            the input graph.

    """
    S = ctl.linkedCycles_tools()
    S.G = nx.Graph(nx_graph)
    basis_nx = S.construct_networkx_minimum_basis()

    return basis_nx


def extract_linkage_matrix(numeric_res):
    """
    Compute the linkage matrix from raw, non-rounded resuts dict structure.

    Args:
        numeric_res (networkx.Graph):\n
            The linkage dictionary, contaitning the non-rounded results of the
            Gauss-Map calculations for each cycle pair.

    Returns:
        ndarray:\n
            The linkage matrix of two graphs in cycle per cycle representation.

    """
    d1 = set([k[0] for k in numeric_res.keys()])
    d2 = set([k[1] for k in numeric_res.keys()])
    nr = np.zeros((len(d1), len(d2)))

    for i in sorted(d1):
        for j in sorted(d2):
            nr[i, j] = np.round(numeric_res[(i, j)], 0)

    return nr


def calc_basis_linkage(cycle_sets1, cycle_sets2):
    """
    Compute the linkage dictionary for each cycle pair.

    Args:
        cycle_sets1 (list):\n
            A list of networkx.Graph objects, represting the basis cycles of
            the input graph #1.
        cycle_sets2 (list):\n
            A list of networkx.Graph objects, represting the basis cycles of
            the input graph #2.

    Returns:
        dict:\n
            The linkage dictionary, contaitning the non-rounded results of the
            Gauss-Map calculations for each cycle pair.

    """
    # calc linkage of basis cycles
    T = ctl.linkedCycles_extraTools()
    bool_res, res = T.calc_linkage_cycleSets_nxGraph(cycle_sets1, cycle_sets2)

    return res
