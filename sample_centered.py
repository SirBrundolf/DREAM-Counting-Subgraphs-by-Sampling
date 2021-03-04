# Algorithm 3: sample-centered
###############################################################
# Def: L(u, v) = Neighbors of u greater than v, e = (u, v) ∈ E.
# Def: λe = L(u, v) * L(v, u), Λ = sum(λe for each e).
###############################################################
# 1 Compute λe for all edges and set pe = λe / Λ.
# 2 Pick edge e = (u, v) with probability pe.
# 3 Pick uniform random neighbor u' of u such that v < u'.
# 4 Pick uniform random neighbor v' of v such that u < v'.
# 5 Output the three edges {(u', u), (u, v), (v, v')}.


import numpy as np
import random


big_lambda = 0
lambda_list = np.array([])


def init_sample_centered(g):
    global big_lambda, lambda_list

    big_lambda = 0
    lambda_list = np.array([])
    calculate_big_lambda(g)


def sample_centered(g, edges, k):
    edges_picked = random.choices(edges, weights=lambda_list, k=k)
    samples = []
    for e in edges_picked:
        u, v = e[0], e[1]
        degree_u = g.degree(u)
        degree_v = g.degree(v)
        neighbors_of_u_bigger_than_v = [neighbor for neighbor in g[u] if degree_v < g.degree(neighbor)
                                        or (degree_v == g.degree(neighbor) and v < neighbor)]
        neighbors_of_v_bigger_than_u = [neighbor for neighbor in g[v] if degree_u < g.degree(neighbor)
                                        or (degree_u == g.degree(neighbor) and u < neighbor)]
        if len(neighbors_of_u_bigger_than_v) == 0 or len(neighbors_of_v_bigger_than_u) == 0:
            edges_picked.append(random.choices(edges, weights=lambda_list, k=1)[0])
            continue
        u_ = neighbors_of_u_bigger_than_v[np.random.randint(len(neighbors_of_u_bigger_than_v))]
        v_ = neighbors_of_v_bigger_than_u[np.random.randint(len(neighbors_of_v_bigger_than_u))]
        centered_three_path = [(u_, u), (u, v), (v, v_)]
        if centered_three_path is not None:
            samples.append(centered_three_path)
        else:
            edges_picked.append(random.choices(edges, weights=lambda_list, k=1)[0])
    return samples


def calculate_big_lambda(g):
    global big_lambda
    global lambda_list

    for edge in g.edges:
        l_uv = sum([1 for neighbor in g[edge[0]] if neighbor > edge[1]])
        l_vu = sum([1 for neighbor in g[edge[1]] if neighbor > edge[0]])
        lambda_e = l_uv * l_vu
        lambda_list = np.append(lambda_list, lambda_e)
        big_lambda += lambda_e
    lambda_list = lambda_list / big_lambda
