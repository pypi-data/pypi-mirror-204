# @Author:  Felix Kramer
# @Date:   2021-11-27T20:10:14+01:00
# @Email:  kramer@mpi-cbg.de
# @Project: go-with-the-flow
# @Last modified by:    Felix Kramer
# @Last modified time: 2021-11-28T21:53:35+01:00
# @License: MIT

import sys
import os.path as op
import networkx as nx
import numpy as np
import scipy

import kirchhoff.circuit_init as kfi
import kirchhoff.circuit_dual as kcd
import kirchhoff.init_dual as kci

bouncerList = []

def set_print_labels(D):
    
    for i, khf in enumerate(D.layer):

        khf.nodes['label'] = [n for n in khf.G.nodes()]
        khf.edges['label'] = [e for i, e in enumerate(khf.G.edges())]  
    
    return D

def createLabelCatenation(num_periods):

    nx_type = 'catenation'
    D = kcd.initialize_dual_from_catenation(dual_type=nx_type, num_periods=num_periods)

    D = set_print_labels(D)

    return D

def createHexagonal(num_periods=2):

    K=kfi.initialize_circuit_from_crystal('hexagonal',num_periods)

    for n in K.G.nodes():
        p=K.G.nodes[n]['pos']
        K.G.nodes[n]['pos']=np.array([*p,0.])

    return K

def createHexagon(num_periods=2):

    K=kfi.initialize_circuit_from_crystal('hexagonal',num_periods)
    for n in K.G.nodes():
        p = K.G.nodes[n]['pos']
        K.G.nodes[n]['pos']=np.array([*p,0.])

    global bouncerList
    for bl in bouncerList:
        K.G.remove_edge(*bl)

    list_n = [n for n in K.G.nodes() if K.G.degree(n)==0]
    for n in list_n:
        K.G.remove_node(n)

    return K

def createLabelDiamond(num_periods):

    nx_type = 'diamond'
    D = kcd.initialize_dual_from_minsurf(dual_type=nx_type, num_periods=num_periods)

    D = set_print_labels(D)

    return D
                
def createLabelLaves(num_periods):

    nx_type = 'laves'
    D = kcd.initialize_dual_from_minsurf(dual_type=nx_type, num_periods=num_periods)

    D = set_print_labels(D)

    return D

def createLabelSimple(num_periods):

    nx_type = 'simple'
    D1 = kcd.initialize_dual_from_minsurf(dual_type=nx_type, num_periods=num_periods)
    
    d = kci.NetworkxDual()
    d.layer = [khf.G for khf in D1.layer]
            
    D = kcd.DualCircuit(kcd.construct_from_graphSet(d))
    D = set_print_labels(D)
    
    return D

def createLabelHexagonHopfed(num_hex=4, num_ring=20, coord_ring=[2.5, 2.5, 4.25]):

    K = createHexagon(num_hex)
    G1 = K.G
    ##### generate intertwined curves
    phi=np.linspace(0,1,num=num_ring)*2.*np.pi
    R=coord_ring[0]

    # unlink
    G0 = nx.Graph()
    for i,p in enumerate(phi[:-1]):
        XYZ = (coord_ring[1],coord_ring[2]+R*np.cos(p),np.sin(p)*R)
        G0.add_node(i, pos=np.array(XYZ))

    for i,p in enumerate(phi[:-2]):
        G0.add_edge(i, i+1)

    G0.add_edge(len(phi)-2, 0)

    d = kci.NetworkxDual()
    d.layer = [G0, G1]
    D = kcd.DualCircuit(kcd.construct_from_graphSet(d))

    D = set_print_labels(D)
    return D