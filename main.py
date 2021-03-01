import networkx as nx
import three_path_sampler
import centered_sampler
import time


c_basic = [0, 0, 0, 0, 0, 0]
c_advanced = [0, 0, 0, 0, 0, 0]
limit = 0

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

with open("Datasets/facebook_combined.txt") as test_graph:
    for line in test_graph:
        line = line.rstrip()
        vertices = line.split(" ")
        if vertices[0] != vertices[1]:
            g.add_edge(vertices[0], vertices[1])

start_time = time.time()


print(len(g.nodes))
print(len(g.edges))
print("Read file")
three_path_sampler.init_three_path_sampler(g)
print("Initialized 3-path-sampler")
first_c_basic = three_path_sampler.three_path_sampler(g, g, 2000)  #k = 200.000 on original paper
print("3-path-sampler done")
c_basic[0], c_basic[1], c_basic[2] = first_c_basic[0], first_c_basic[1], first_c_basic[2]
#c_basic[0], c_basic[1], c_basic[2], c_basic[3], c_basic[4], c_basic[5] = \
#    first_c_basic[0], first_c_basic[1], first_c_basic[2], first_c_basic[3], first_c_basic[4], first_c_basic[5]
centered_sampler.init_centered_sampler(g)
print("Initialized centered-sampler")
last_c_basic = centered_sampler.centered_sampler(g, g, 2000)
print("Centered-sampler done")
c_basic[3], c_basic[4], c_basic[5] = last_c_basic[3], last_c_basic[4], last_c_basic[5]

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
total = 0
for u, v, p in predictions:
    total += p
avg = total/len(predictions)
limit = (avg - min_prediction) / (max_prediction - min_prediction)
print(min_prediction)
print(max_prediction)
print(limit)
for u, v, p in predictions:
    normalized_p = (p - min_prediction) / (max_prediction - min_prediction)
    if normalized_p >= limit:
        g_filtered.add_edge(u, v)
print(len(g.nodes))
print(len(g.edges))
three_path_sampler.init_three_path_sampler(g_filtered)
print("Initialized 3-path-sampler")
first_c_advanced = three_path_sampler.three_path_sampler(g, g_filtered, 2000)
print("3-path-sampler done")
c_advanced[0], c_advanced[1], c_advanced[2] = first_c_advanced[0], first_c_advanced[1], first_c_advanced[2]
centered_sampler.init_centered_sampler(g_filtered)
print("Initialized centered-sampler")
last_c_advanced = centered_sampler.centered_sampler(g, g_filtered, 2000)
print("Centered-sampler done")
c_advanced[3], c_advanced[4], c_advanced[5] = last_c_advanced[3], last_c_advanced[4], last_c_advanced[5]

print("Improved Algorithm Results: ", c_advanced)
"""


print("--- %s seconds ---" % (time.time() - start_time))
