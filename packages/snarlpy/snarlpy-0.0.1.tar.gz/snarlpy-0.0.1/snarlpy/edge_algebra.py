# @Author:  Felix Kramer
# @Date:   2021-09-25T14:20:58+02:00
# @Email:  kramer@mpi-cbg.de
# @Project: entanglement-analysis
# @Last modified by:   felix
# @Last modified time: 2022-07-28T15:11:15+02:00
# @License: MIT
import numpy as np
import snarlpy.signature as signature


def edge_column(c, edge_set, sig_graph):
    """
    Compute the signature-sensitive edge vector representation of a given
    cycle.

    Args:
        c (networkx.Graph): \n
            A networkx.Graph representing a Eulerian cycle in the simple
            graph.
        edge_set (list): \n
            A list of all edges in the simple graph.
        sig_graph (dict): \n
            A dictionary holding the information on the graph's intrinsic
            edge signatures (directions) for comparison with cycle edge
            directions.

    Returns:
        nadarray: \n
            The signature-sensitive edge vector representation of the given
            cycle.

    """

    e_row = np.zeros(len(edge_set))
    signa = signature.get_signature(c, sig_graph)

    for i, e in enumerate(edge_set):

        if c.has_edge(*e):

            if e in signa.keys():
                e_row[i] = signa[e]
            else:
                e_row[i] = signa[e[::-1]]

    return e_row


def edge_column_rand(c, edge_set, sig_graph):
    """
    Compute the signature-sensitive edge vector representation of a given
    cycle. Randomize the initial node for the ycle's signature computation.

    Args:
        c (networkx.Graph): \n
            A networkx.Graph representing a Eulerian cycle in the simple
            graph.
        edge_set (list): \n
            A list of all edges in the simple graph.
        sig_graph (dict): \n
            A dictionary holding the information on the graph's intrinsic
            edge signatures (directions) for comparison with cycle edge
            directions.

    Returns:
        nadarray: \n
            The signature-sensitive edge vector representation of the given
            cycle.

    """
    e_row = np.zeros(len(edge_set))
    signa = signature.get_signature_rand(c, sig_graph)

    for i, e in enumerate(edge_set):

        if c.has_edge(*e):

            if e in signa.keys():
                e_row[i] = signa[e]

            else:
                e_row[i] = signa[e[::-1]]

    return e_row


def generate_edge_matrix(basis, edge_set, sig_graph):
    """
    Compute the signature-sensitive edge vector representations of an entire
    cycle basis.

    Args:
        basis (list): \n
            A list networkx.Graph objects, representing the Eulerian cycle
            basis of the simple graph.
        edge_set (list): \n
            A list of all edges in the simple graph.
        sig_graph (dict): \n
            A dictionary holding the information on the graph's intrinsic
            edge signatures (directions) for comparison with cycle edge
            directions.

    Returns:
        nadarray: \n
            The signature-sensitive edge vectors of all cycles bundled into one
            matrix (technically the graph's mesh matrix)
    """
    rows = len(basis)
    cols = len(edge_set)
    E = np.zeros((rows, cols))

    for i, c in enumerate(basis):
        E[i] = edge_column(c, edge_set, sig_graph)

    return E.T


def edge_column_binary(c, edge_set):
    """
    Compute the binary edge vector representation of a given
    cycle.

    Args:
        c (networkx.Graph): \n
            A networkx.Graph representing a Eulerian cycle in the simple
            Graph.
        edge_set (list): \n
            A list of all edges in the simple graph.

    Returns:
        nadarray: \n
            The binary edge vector representation of the given
            cycle.

    """
    e_row = np.zeros(len(edge_set))

    idx = [i for i, e in enumerate(edge_set) if c.has_edge(*e)]
    e_row[idx] = 1

    return e_row


def generate_edge_matrix_binary(basis, edge_set):
    """
    Compute the binary edge vector representations of an entire
    cycle basis.

    Args:
        basis (list): \n
            A list networkx.Graph objects, representing the Eulerian cycle
            basis of the simple graph.
        edge_set (list): \n
            A list of all edges in the simple graph.

    Returns:
        nadarray: \n
            The binary edge vectors of all cycles bundled into one
            matrix (technically the graph's mesh matrix).
    """
    rows = len(basis)
    cols = len(edge_set)
    E = np.zeros((rows, cols))

    for i, c in enumerate(basis):
        E[i] = edge_column_binary(c, edge_set)

    return E


def get_cycle_superpositions_edge_vector(keys, cycle_matrix):
    """
    Compute the edge vector of a cycle aquired from superposition of basis
    cycles.

    Args:
        keys (list): \n
            An index list indicating which cycles are to be superimposed.
        cycle_matrix (ndarray): \n
            The binary edge vectors of all cycles bundled into one
            matrix (technically the graph's mesh matrix).

    Returns:
        nadarray: \n
            The signature-sensitive edge vectors of all cycles bundled into one
            matrix (technically the graph's mesh matrix)
    """
    idx = [i for i, k in enumerate(keys) if k == 1]
    E = np.sum(cycle_matrix[idx], axis=0)

    return np.mod(E, 2)


def check_superposition_edge_connected(keys, edge_matrix):
    """
    Compute cycle superpostion with consectuive test whether the cycles
    generated during superposition are connected.

    Args:
        keys (list): \n
            An index list indicating which cycles are to be superimposed.
        cycle_matrix (ndarray): \n
            The binary edge vectors of all cycles bundled into one
            matrix (technically the graph's mesh matrix).

    Returns:
        bool: \n
            True or False, depending on whether the cycles
            generated during superposition are connected.
    """
    idx = [i for i, k in enumerate(keys) if k == 1]
    checking = [False]*len(idx)
    checking[0] = True

    if len(idx) > 1:

        E_aux = edge_matrix[idx[0]]
        for i, id in enumerate(idx[1:]):

            E = np.add(E_aux, edge_matrix[id])
            if len(np.where(E > 1)[0]) > 0:
                E_aux = np.mod(E, 2)
                checking[i+1] = True
            else:
                break

    result = False
    if all(checking):
        result = True

    return result


def sort_rows(column, idx, Ax):
    """
    Resort rows, as part of acquiring the echelon form of the linear system Ax.

    Args:
        column (ndarray): \n
            Current column index being processed.
        idx (ndarray): \n
            The current row processed that needs to be shifted.
        Ax (ndarray): \n
            A given binary equation system, used for linear independence tests
            of Eulerian cycles.
    """
    Ax[[column, idx], :] = Ax[[idx, column], :]


def calc_echelon_form(Ax):
    """
    Compute the echelon form of a given binary equations system and checking
    for inconsistencies and solutions of the key problem.

    Args:
        Ax (ndarray): \n
            A given binary equation system, used for linear independence tests
            of Eulerian cycles.

    Returns:
        ndarray: \n
            The last column of the echelon, indicating whether the column
            vectors are linear independent or not.
    """
    columns = len(Ax[0, :])

    # compute echelon
    for column in range(0, columns-1):

        idx_nz = np.nonzero(Ax[column:, column])[0]
        idx = idx_nz[0]+column

        if len(idx_nz) > 1:

            new_idx = idx_nz[1:]+column
            aux = np.add(Ax[new_idx], Ax[idx])
            Ax[new_idx] = np.mod(aux, 2)

        sort_rows(column, idx, Ax)

    # compute solution
    Ax = Ax[:columns-1, :]

    for column in range(1, columns-1):

        c = columns-1-column
        idx_nz = np.nonzero(Ax[:c, c])[0]

        aux = np.add(Ax[idx_nz], Ax[c])
        Ax[idx_nz] = np.mod(aux, 2)

    return Ax[:, -1]


def get_component_key(edge_vector, edge_matrix):
    """
    For a given binary edge vector, compute its coefficient vector
    with respect to the currently used basis.

    Args:
        edge_vector (ndarray): \n
            The binary edge vector presentation of an Eulerian cycle.
        edge_matrix (ndarray): \n
            The simple graph's mesh matrix, representing the set of basis
            cycles.

    Returns:
        ndarray: \n
            The coefficient vector for given cycle in the current
            cycle basis.
    """
    Ax = np.concatenate(
        (
            edge_matrix.T, np.array([edge_vector]).T), axis=1
        )

    new_key = calc_echelon_form(Ax)

    return new_key
