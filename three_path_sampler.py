# Algorithm 2: 3-path-sampler
#################################################################################################################
# Def: G = (V, E)
#################################################################################################################
# 1 Run 'sample' k times to get k sets of edges. Let Sl denote the set of corresponding vertices for the lth set.
# 2 Initialize counti = 0 for i ∈ [2, 6].
# 3 For l ∈ [1, k],
# 4     Determine subgraph induced by Sl.
# 5     If this is the ith motif, increment counti.
# 6 For each i ∈ [2, 6],
# 7     Set Ci = (counti / k) * (W / A(2, i)).
# 8 Set N1 = sum(C(dv, 3) for each v ∈ V).
# 9 Set(induced 3 - stars) C1 = N1 − C3 − 2 * C5 − 4 * C6.


import numpy as np
import scipy.special as sp
import sample

import motif_types
import networkx as nx
from networkx.algorithms import isomorphism



a = np.array([0, 1, 2, 4, 6, 12], dtype=np.uint64)  #3-path counts in all other motifs
c = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)  #Induced subgraph counts for all motifs
count = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)  #Induced subgraph counts of k samples


def init_three_path_sampler(g):
    global a, c, count

    a = np.array([0, 1, 2, 4, 6, 12], dtype=np.uint64)
    c = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)
    count = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)
    sample.init_sample(g)


def three_path_sampler(g, g_filtered, k):
    global c

    w = sample.w
    edges = list(g_filtered.edges)
    three_paths = sample.sample(g_filtered, edges, k)   #Get k three-paths by calling sample
    print("Got three-paths")
    determine_induced_subgraph(three_paths, g)   #For each three-path, determine the induced subgraph
    print("Determining induced subgraphs done")
    for i in range(1, 6):
        c[i] = (count[i] / k) * (w / a[i])   #Calculate c from counts (ci = (counti / k) * (W / A(2, i)))
    print("C1-5's calculated")
    n1 = sum([sp.comb(g.degree(v), 3) for v in g.nodes])   #Set n1 = sum(c(dv, 3) for each v ∈ V)
    print("N1 calculated")
    c[0] = n1 - (c[2] + 2 * c[4] + 4 * c[5])  #Calculate c0 from n1 − c3 − 2 * c5 − 4 * c6
    print("C0 calculated")
    return c


def determine_induced_subgraph(three_paths, g):
    for three_path in three_paths:
        vertices = [three_path[0][0], three_path[1][0], three_path[1][1], three_path[2][1]]  #Get unique vertices from three paths
                                                                                      #Ex. get u, v, y, x from edges u-v, v-y, y-x
        edges = g.edges(vertices)  #Find all the edges that contains any of those vertices
        subgraph = nx.Graph()
        for edge in edges:  #For each edge, check if both of the nodes are in vertices list and if true, add them to the induced subgraph
            if edge[0] in vertices and edge[1] in vertices:
                subgraph.add_edge(edge[0], edge[1])
        for i in range(len(motif_types.motifs)):  #Compare our induced subgraph with each of the motifs
            graph_matcher = isomorphism.GraphMatcher(subgraph, motif_types.motifs[i])
            if graph_matcher.is_isomorphic():
                count[i + 1] += 1
                break
