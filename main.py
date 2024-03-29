import networkx as nx
import three_path_sampler
import centered_sampler
import time


#c_basic and c_advanced will be our subgraph counts, c_basic is for original algorithm, c_advanced for improved
c_basic = [0, 0, 0, 0, 0, 0]
c_advanced = [0, 0, 0, 0, 0, 0]
limit = 0

g = nx.Graph()

#Reading the dataset
with open("Datasets/facebook_combined.txt") as test_graph:
    for line in test_graph:
        line = line.rstrip()
        vertices = line.split(" ")
        if vertices[0] != vertices[1]:  #No self-loops are allowed
            g.add_edge(vertices[0], vertices[1])

start_time = time.time()


#Original Algorithm

print("Read file")
print("Node Counts:", len(g.nodes))
print("Edge Counts:", len(g.edges))

three_path_sampler.init_three_path_sampler(g)
print("Initialized 3-path-sampler")
first_c_basic = three_path_sampler.three_path_sampler(g, g, 2000)  #k = 200.000 on original paper, 2000 gives us good enough results
print("3-path-sampler done")
c_basic[0], c_basic[1], c_basic[2], c_basic[3], c_basic[4], c_basic[5] = \
    first_c_basic[0], first_c_basic[1], first_c_basic[2], first_c_basic[3], first_c_basic[4], first_c_basic[5]
    
# Old calculation for cycle-based motifs with centered_sampler
#c_basic[0], c_basic[1], c_basic[2] = first_c_basic[0], first_c_basic[1], first_c_basic[2]
#centered_sampler.init_centered_sampler(g)
#print("Initialized centered-sampler")
#last_c_basic = centered_sampler.centered_sampler(g, g, 20000)
#print("Centered-sampler done")
#c_basic[3], c_basic[4], c_basic[5] = last_c_basic[3], last_c_basic[4], last_c_basic[5]

print("Original Algorithm Results: ", c_basic)


"""
#Improved Algorithm

print("Read file")
print("Node Counts:", len(g.nodes))
print("Edge Counts:", len(g.edges))

g_filtered = nx.Graph()
g_filtered.add_nodes_from(g)   #Create a new graph g_filtered with all the vertices of graph g
predictions = list(nx.adamic_adar_index(g, g.edges))
pred_p = [p for u, v, p in predictions]
max_prediction = max(pred_p)
min_prediction = min(pred_p)
avg = sum(pred_p)/len(pred_p)
limit = (avg - min_prediction) / (max_prediction - min_prediction)  #Calculate the limiting score with normalization
print("Min. Score:", min_prediction)
print("Max. Score:", max_prediction)
print("Limiting Score (Normalized):", limit)
for u, v, p in predictions:  #For every edge, add only the edges with similarity score greater than average to g_filtered
    normalized_p = (p - min_prediction) / (max_prediction - min_prediction)   #Normalize the score beween 0 and 1
    if normalized_p >= limit:
        g_filtered.add_edge(u, v)

three_path_sampler.init_three_path_sampler(g_filtered)
print("Initialized 3-path-sampler")
first_c_advanced = three_path_sampler.three_path_sampler(g, g_filtered, 2000)
print("3-path-sampler done")
c_advanced[0], c_advanced[1], c_advanced[2], c_advanced[3], c_advanced[4], c_advanced[5] = \
    first_c_advanced[0], first_c_advanced[1], first_c_advanced[2], first_c_advanced[3], first_c_advanced[4], first_c_advanced[5]

# Old calculation for cycle-based motifs with centered_sampler
#c_advanced[0], c_advanced[1], c_advanced[2] = first_c_advanced[0], first_c_advanced[1], first_c_advanced[2]
#centered_sampler.init_centered_sampler(g_filtered)
#print("Initialized centered-sampler")
#last_c_advanced = centered_sampler.centered_sampler(g, g_filtered, 2000)
#print("Centered-sampler done")
#c_advanced[3], c_advanced[4], c_advanced[5] = last_c_advanced[3], last_c_advanced[4], last_c_advanced[5]

print("Improved Algorithm Results: ", c_advanced)
"""


print("--- %s seconds ---" % (time.time() - start_time))
