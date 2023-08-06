# @Author:  Felix Kramer
# @Date:   2021-09-25T14:20:58+02:00
# @Email:  kramer@mpi-cbg.de
# @Project: go-with-the-flow
# @Last modified by:   felix
# @Last modified time: 2022-07-28T18:41:23+02:00
# @License: MIT
import networkx as nx
import numpy as np
import scipy
import snarlpy.sampling as itws


def getEdgeLinkageOperator(graph_sets):
    """
    Compute the linkage matrices, both in edge space and cycle space
    representation.

    Args:
        graph_sets (list):\n
            A list of networkx.Graph objects.

    Returns:
        ndarray:\n
            The linkage matrix in edge space representation.
        ndarray:\n
            The linkage matrix in cycle space representation.

    """
    cyc_nx_base, lk_mat = itws.calc_basisIntertwinedness(graph_sets)
    graph_matrices = itws.get_basis_matrices(graph_sets, cyc_nx_base)

    cyc_mat_dir = [cm for cm in graph_matrices[-2]]
    cyc_mat_inv = [scipy.linalg.pinv(cm) for cm in cyc_mat_dir]

    P = np.dot(np.dot(cyc_mat_inv[0].T, lk_mat), cyc_mat_inv[1])

    return P, lk_mat


def cuttingEdgeAlgorithm(cut_graph, ref_graph):
    """
    Compute the optimal cuts set for a graph in an intertwined structure.

    Args:
        cut_graph (list):\n
            The graph for which the optimal cut set if searched.
        ref_graph (list):\n
            The reference graph, which is setting the frame to be disentangled
            from.

    Returns:
        list:\n
            The list of optimal cut set for the cut_graph.

    """
    cuts = []
    linked = True
    G1 = nx.Graph(cut_graph)
    G2 = nx.Graph(ref_graph)

    nullity = itws.calc_nullity(G1)

    while linked:

        linkage_components = []
        cut_candidates = {}
        cc = [G1.subgraph(c).copy() for c in nx.connected_components(G1)]

        for i, g in enumerate(cc):

            P, lk_mat = getEdgeLinkageOperator([g, G2])

            if not np.all(lk_mat == 0.):
                linkage_components.append(P)

        if len(linkage_components) == 0:
            linked = False
            break

        for P in linkage_components:
            I = np.diagonal(np.dot(P, P.T))
            maxPriority = np.amax(I)
            idx = np.argmax(I)
            cut_candidates[idx] = maxPriority

        idx = max(cut_candidates, key=cut_candidates.get)
        cuts.append(find_edge_byIndex(G1, idx))

        G1.remove_edge(*cuts[-1])
        if len(cuts) == nullity:
            linked = False
            break

    return cuts


def find_edge_byIndex(G, idx):
    """
    Finde edge by label.

    Args:
        G (networkx.Graph):\n
            A simple graph.
        idx (int):\n
            An edge label to be searched for.

    Returns:
        tuple:\n
            A networkx.Graph edge tuple.

    """
    for i, e in enumerate(G.edges()):
        if i == idx:
            return e
    return -1
