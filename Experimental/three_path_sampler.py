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



a = np.array([0, 1, 2, 4, 6, 12], dtype=np.uint64)
c = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)
count = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)


def init_three_path_sampler(g):
    global a, c, count

    a = np.array([0, 1, 2, 4, 6, 12], dtype=np.uint64)
    c = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)
    count = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)
    sample.init_sample(g)


def three_path_sampler(g, g_filtered, k):
    global c

    w = sample.w
    three_paths = []
    edges = list(g.edges)
    for _ in range(k):
        three_paths.append(sample.sample(g_filtered, edges))
        #print(_)
    print("Got three-paths")
    for three_path in three_paths:
        index = determine_induced_subgraph(three_path, g)
        if index != -1:
            count[index] += 1
    print("Determining induced subgraphs done")
    for i in range(1, 6):
        c[i] = (count[i] / k) * (w / a[i])
    print("C1-5's calculated")
    n1 = sum([sp.comb(g.degree(v), 3) for v in g.nodes])
    print("N1 calculated")
    c[0] = n1 - (c[2] + 2 * c[4] + 4 * c[5])
    print("C0 calculated")
    #for i in range(len(motif_types.motifs)):
    #    print((w/c[i])**2)
    #for i in range(6):
    #    print(count[i])
    return c


def determine_induced_subgraph(three_path, g):
    vertices = [three_path[0][0], three_path[1][0], three_path[1][1], three_path[2][1]]
    edges = g.edges(vertices)
    subgraph = nx.Graph()
    for edge in edges:
        if edge[0] in vertices and edge[1] in vertices:
            subgraph.add_edge(edge[0], edge[1])
    for i in range(len(motif_types.motifs)):
        graph_matcher = isomorphism.GraphMatcher(subgraph, motif_types.motifs[i])
        if graph_matcher.is_isomorphic():
            return i + 1
    return -1
