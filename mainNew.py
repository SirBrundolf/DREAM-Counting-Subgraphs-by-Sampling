import numpy as np
import scipy.special as sp
import motif_types
import networkx as nx
from networkx.algorithms import isomorphism
import three_path_sampler
import centered_sampler
import time


c_basic = [0, 0, 0, 0, 0, 0]
c_advanced = [0, 0, 0, 0, 0, 0]
limit = 0.05
k = 2000

"""
#g = nx.complete_graph(5)
g = nx.Graph()
g.add_edge(1, 2)
g.add_edge(1, 3)
g.add_edge(1, 4)
g.add_edge(2, 3)
g.add_edge(3, 4)
g.add_edge(2, 5)
g.add_edge(4, 5)
g.add_edge(5, 6)
"""

g = nx.Graph()

with open("facebook_combined.txt") as test_graph:
    for line in test_graph:
        line = line.rstrip()
        vertices = line.split(" ")
        if vertices[0] != vertices[1]:
            g.add_edge(vertices[0], vertices[1])

start_time = time.time()

print(len(g.nodes))
print(len(g.edges))
print("Read file")


w = 0
tau_list = np.array([])

a = np.array([0, 1, 2, 4, 6, 12], dtype=np.uint64)
c1 = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)
count1 = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)

for edge in g.edges:
    tau_e = (g.degree(edge[0]) - 1) * (g.degree(edge[1]) - 1)
    tau_list = np.append(tau_list, tau_e)
    w += tau_e
tau_list = tau_list / w

print("Initialized 3-path-sampler")

three_paths = []
for _ in range(k):
    e = np.random.default_rng().choice(g.edges, 1, p=tau_list)
    u = e[0][0]
    v = e[0][1]
    neighbors_of_u_except_v = list(set(g[u]).difference({v}))
    neighbors_of_v_except_u = list(set(g[v]).difference({u}))
    u_ = neighbors_of_u_except_v[np.random.randint(len(neighbors_of_u_except_v))]
    v_ = neighbors_of_v_except_u[np.random.randint(len(neighbors_of_v_except_u))]
    if u_ == v_:
        _ = _ - 1
        continue
    three_paths.append([(u_, u), (u, v), (v, v_)])
print("Got three-paths")
for three_path in three_paths:
    index = -1
    vertices = [three_path[0][0], three_path[1][0], three_path[1][1], three_path[2][1]]
    edges = g.edges(vertices)
    subgraph = nx.Graph()
    for edge in edges:
        if edge[0] in vertices and edge[1] in vertices:
            subgraph.add_edge(edge[0], edge[1])
    for i in range(len(motif_types.motifs)):
        graph_matcher = isomorphism.GraphMatcher(subgraph, motif_types.motifs[i])
        if graph_matcher.is_isomorphic():
            index = i + 1
    if index != -1:
        count1[index] += 1
print("Determining induced subgraphs done")
for i in range(1, 3):
    c1[i] = (count1[i] / k) * (w / a[i])
print("C1-5's calculated")
n1 = sum([sp.comb(g.degree(v), 3) for v in g.nodes])
print("N1 calculated")
c1[0] = n1 - (c1[2] + 2 * c1[4] + 4 * c1[5])
print("C0 calculated")

print("3-path-sampler done")
c_basic[0], c_basic[1], c_basic[2] = c1[0], c1[1], c1[2]


big_lambda = 0
lambda_list = np.array([])

b = np.array([0, 0, 0, 1, 1, 3], dtype=np.uint64)
c2 = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)
count2 = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)

for edge in g.edges:
    l_uv = sum([1 for neighbor in g[edge[0]] if neighbor > edge[1]])
    l_vu = sum([1 for neighbor in g[edge[1]] if neighbor > edge[0]])
    lambda_e = l_uv * l_vu
    lambda_list = np.append(lambda_list, lambda_e)
    big_lambda += lambda_e
lambda_list = lambda_list / big_lambda

print("Initialized centered-sampler")

centered_three_paths = []
for _ in range(k):
    e = np.random.default_rng().choice(g.edges, 1, p=lambda_list)
    u = e[0][0]
    v = e[0][1]
    neighbors_of_u_bigger_than_v = [neighbor for neighbor in g[u] if g.degree(v) < g.degree(neighbor)
                                    or (g.degree(v) == g.degree(neighbor) and v < neighbor)]
    neighbors_of_v_bigger_than_u = [neighbor for neighbor in g[v] if g.degree(u) < g.degree(neighbor)
                                    or (g.degree(u) == g.degree(neighbor) and u < neighbor)]
    if len(neighbors_of_u_bigger_than_v) == 0 or len(neighbors_of_v_bigger_than_u) == 0:
        _ = _ - 1
        continue
    u_ = neighbors_of_u_bigger_than_v[np.random.randint(len(neighbors_of_u_bigger_than_v))]
    v_ = neighbors_of_v_bigger_than_u[np.random.randint(len(neighbors_of_v_bigger_than_u))]
    if [(u_, u), (u, v), (v, v_)] is not None:
        centered_three_paths.append([(u_, u), (u, v), (v, v_)])
print("Got centered-three-paths")
for centered_three_path in centered_three_paths:
    index = -1
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
            index = i + 1
    if index != -1:
        count2[index] += 1
print("Determining induced subgraphs done")
for i in range(3, 6):
    c2[i] = (count2[i] / k) * (big_lambda / b[i])
print("C3-5's calculated")

print("Centered-sampler done")
c_basic[3], c_basic[4], c_basic[5] = c2[3], c2[4], c2[5]

print("Original Algorithm Results: ", c_basic)


"""
g_filtered = nx.Graph()
g_filtered.add_nodes_from(g)
predictions = list(nx.adamic_adar_index(g, g.edges))
max_prediction = 0
min_prediction = 999
for u, v, p in predictions:
    if min_prediction == 999 or p < min_prediction:
        min_prediction = p
    if p > max_prediction:
        max_prediction = p
for u, v, p in predictions:
    normalized_p = (p - min_prediction) / (max_prediction - min_prediction)
    if normalized_p >= limit:
        g_filtered.add_edge(u, v)


w = 0
tau_list = np.array([])

a = np.array([0, 1, 2, 4, 6, 12], dtype=np.uint64)
c = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)
count = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)

for edge in g_filtered.edges:
    tau_e = (g_filtered.degree(edge[0]) - 1) * (g_filtered.degree(edge[1]) - 1)
    tau_list = np.append(tau_list, tau_e)
    w += tau_e
tau_list = tau_list / w

print("Initialized 3-path-sampler")

three_paths = []
for _ in range(k):
    e = np.random.default_rng().choice(g_filtered.edges, 1, p=tau_list)
    u = e[0][0]
    v = e[0][1]
    neighbors_of_u_except_v = list(set(g_filtered[u]).difference({v}))
    neighbors_of_v_except_u = list(set(g_filtered[v]).difference({u}))
    u_ = neighbors_of_u_except_v[np.random.randint(len(neighbors_of_u_except_v))]
    v_ = neighbors_of_v_except_u[np.random.randint(len(neighbors_of_v_except_u))]
    if u_ == v_:
        continue
    three_paths.append([(u_, u), (u, v), (v, v_)])
print("Got three-paths")
for three_path in three_paths:
    index = -1
    vertices = [three_path[0][0], three_path[1][0], three_path[1][1], three_path[2][1]]
    edges = g.edges(vertices)
    subgraph = nx.Graph()
    for edge in edges:
        if edge[0] in vertices and edge[1] in vertices:
            subgraph.add_edge(edge[0], edge[1])
    for i in range(len(motif_types.motifs)):
        graph_matcher = isomorphism.GraphMatcher(subgraph, motif_types.motifs[i])
        if graph_matcher.is_isomorphic():
            index = i + 1
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

print("3-path-sampler done")
c_advanced[0], c_advanced[1], c_advanced[2] = c[0], c[1], c[2]



big_lambda = 0
lambda_list = np.array([])

b = np.array([0, 0, 0, 1, 1, 3], dtype=np.uint64)
c = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)
count = np.array([0, 0, 0, 0, 0, 0], dtype=np.uint64)

for edge in g_filtered.edges:
    l_uv = sum([1 for neighbor in g_filtered[edge[0]] if neighbor > edge[1]])
    l_vu = sum([1 for neighbor in g_filtered[edge[1]] if neighbor > edge[0]])
    lambda_e = l_uv * l_vu
    lambda_list = np.append(lambda_list, lambda_e)
    big_lambda += lambda_e
lambda_list = lambda_list / big_lambda

print("Initialized centered-sampler")

centered_three_paths = []
for _ in range(k):
    e = np.random.default_rng().choice(g_filtered.edges, 1, p=lambda_list)
    u = e[0][0]
    v = e[0][1]
    neighbors_of_u_bigger_than_v = [neighbor for neighbor in g_filtered[u] if g_filtered.degree(v) < g_filtered.degree(neighbor)
                                    or (g_filtered.degree(v) == g_filtered.degree(neighbor) and v < neighbor)]
    neighbors_of_v_bigger_than_u = [neighbor for neighbor in g[v] if g_filtered.degree(u) < g_filtered.degree(neighbor)
                                    or (g_filtered.degree(u) == g_filtered.degree(neighbor) and u < neighbor)]
    if len(neighbors_of_u_bigger_than_v) == 0 or len(neighbors_of_v_bigger_than_u) == 0:
        continue
    u_ = neighbors_of_u_bigger_than_v[np.random.randint(len(neighbors_of_u_bigger_than_v))]
    v_ = neighbors_of_v_bigger_than_u[np.random.randint(len(neighbors_of_v_bigger_than_u))]

    if [(u_, u), (u, v), (v, v_)] is not None:
        centered_three_paths.append([(u_, u), (u, v), (v, v_)])
print("Got centered-three-paths")
for centered_three_path in centered_three_paths:
    index = -1
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
            index = i + 1
    count[index] += 1
print("Determining induced subgraphs done")
for i in range(3, 6):
    c[i] = (count[i] / k) * (big_lambda / b[i])
print("C3-5's calculated")

print("Centered-sampler done")
c_advanced[3], c_advanced[4], c_advanced[5] = c[3], c[4], c[5]

print("Improved Algorithm Results: ", c_advanced)
"""

print("--- %s seconds ---" % (time.time() - start_time))
