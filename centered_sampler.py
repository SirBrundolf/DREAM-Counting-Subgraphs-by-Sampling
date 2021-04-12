# Algorithm 4: centered-sampler
######################################################################################################################
# Def: G = (V, E), B = [0, 0, 0, 1, 1, 3]
######################################################################################################################
# 1 Run 'sample-centered' k times to get k set of edges. Let Tl denote the set of corresponding edges for the lth set.
# 2 Initialize counti = 0 for i ∈ [4, 6].
# 3 For l ∈ [1, k],
# 4     If Tl is a centered 3-path,
# 5         Determine subgraph induced by Tl.
# 6         If this is the ith motif, increment counti.
# 7 For each i ∈ [4, 6],
# 8     Set Ci = (counti / k) · (Λ / Bi).


import numpy as np
import sample_centered

import motif_types
import networkx as nx
from networkx.algorithms import isomorphism

b = np.array([0, 0, 0, 1, 1, 3], dtype=np.uint64)  #4-cycle counts in all other motifs
c = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)  #Induced subgraph counts for cycle-based motifs
count = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)  #Induced subgraph counts of k samples (cycle-based only)


def init_centered_sampler(g):
    global b, c, count

    b = np.array([0, 0, 0, 1, 1, 3], dtype=np.uint64)
    c = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)
    count = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)
    sample_centered.init_sample_centered(g)


def centered_sampler(g, g_filtered, k):
    global c

    big_lambda = sample_centered.big_lambda
    edges = list(g_filtered.edges)
    centered_three_paths = sample_centered.sample_centered(g_filtered, edges, k)  #Get k centered-three-paths
    print("Got centered-three-paths")
    determine_induced_subgraph(centered_three_paths, g)  #For each centered-three-path, determine the induced subgraph
    print("Determining induced subgraphs done")
    for i in range(3, 6):
        c[i] = (count[i] / k) * (big_lambda / b[i])  #Calculate c from counts (ci = (counti / k) · (Λ / Bi))
    print("C3-5's calculated")
    return c


def determine_induced_subgraph(centered_three_paths, g):  #Same method with three_path_sampler's determine_induced_subgraph,
                                                    #except this also checks if the three paths are actually centered or not
    for centered_three_path in centered_three_paths:
        if is_centered_three_path(centered_three_path, g):
            vertices = [centered_three_path[0][0],
                        centered_three_path[1][0],
                        centered_three_path[1][1],
                        centered_three_path[2][1]]
            edges = g.edges(vertices)
            subgraph = nx.Graph()
            for edge in edges:
                if edge[0] in vertices and edge[1] in vertices:
                    subgraph.add_edge(edge[0], edge[1])
            for i in range(len(motif_types.motifs)):
                graph_matcher = isomorphism.GraphMatcher(subgraph, motif_types.motifs[i])
                if graph_matcher.is_isomorphic():
                    count[i + 1] += 1
                    break


def is_centered_three_path(centered_three_path, g):
    u, v = centered_three_path[1][0], centered_three_path[1][1]
    u_, v_ = centered_three_path[0][0], centered_three_path[2][1]
    #Check if neighbor conditions from sample_centered is satisfied (neighbor u' of u, v < u' and neighbor v' of v, u < v')
    if (g.degree(u_) > g.degree(v) and g.degree(v_) > g.degree(u)) \
            or (g.degree(u_) == g.degree(v) and g.degree(v_) == g.degree(u) and u_ > v and v_ > u):
        return True
    return False
