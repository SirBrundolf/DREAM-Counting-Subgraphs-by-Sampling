# Algorithm 1: sample
########################################################################
# Def: e = (u, v) ∈ E, τe = (du − 1) * (dv − 1), W = sum(τe for each e).
########################################################################
# 1 Compute τe for all edges and set pe = τe / W.
# 2 Pick edge e = (u, v) with probability pe.
# 3 Pick uniform random neighbor u' of u other than v.
# 4 Pick uniform random neighbor v' of v other than u.
# 5 Output the three edges {(u', u), (u, v), (v, v')}.


import numpy as np
import random


w = 0
tau_list = np.array([])


def init_sample(g):
    global w, tau_list

    w = 0
    tau_list = np.array([])
    calculate_w(g)


def sample(g, edges, k):  #Getting k samples
    edges_picked = random.choices(edges, weights=tau_list, k=k)   #Pick k edges with probability pe for edge e
    samples = []
    for e in edges_picked:
        u, v = e[0], e[1]
        neighbors_of_u_except_v = [key for key in g[u] if key != v]
        neighbors_of_v_except_u = [key for key in g[v] if key != u]
        u_ = neighbors_of_u_except_v[np.random.randint(len(neighbors_of_u_except_v))]
        v_ = neighbors_of_v_except_u[np.random.randint(len(neighbors_of_v_except_u))]
        if u_ == v_:   #A triangle is found instead of a 3-path, pick another edge
            edges_picked.append(random.choices(edges, weights=tau_list, k=k)[0])
        else:
            samples.append([(u_, u), (u, v), (v, v_)])
    return samples


def calculate_w(g):
    global w
    global tau_list

    for edge in g.edges:
        tau_e = (g.degree(edge[0]) - 1) * (g.degree(edge[1]) - 1)  #(du − 1) * (dv − 1)
        tau_list = np.append(tau_list, tau_e)
        w += tau_e  #sum(τe for each e)
    tau_list = tau_list / w  #pe = τe / W for all edges
