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


def sample(g, edges, k):
    edges = np.random.default_rng().choice(edges, k, p=tau_list)
    res = []
    for e in edges:
        u, v = e[0][0], e[0][1]
        neighbors_of_u_except_v = list(set(g[u]).difference({v}))
        neighbors_of_v_except_u = list(set(g[v]).difference({u}))
        u_ = neighbors_of_u_except_v[np.random.randint(len(neighbors_of_u_except_v))]
        v_ = neighbors_of_v_except_u[np.random.randint(len(neighbors_of_v_except_u))]
        res += [(u_, u), (u, v), (v, v_)]
    return res


def calculate_w(g):
    global w
    global tau_list

    for edge in g.edges:
        tau_e = (g.degree(edge[0]) - 1) * (g.degree(edge[1]) - 1)
        tau_list = np.append(tau_list, tau_e)
        w += tau_e
    tau_list = tau_list / w
