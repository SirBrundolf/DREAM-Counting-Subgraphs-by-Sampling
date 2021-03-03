import networkx as nx

three_star = nx.Graph()
three_star.add_edge(0, 1)
three_star.add_edge(1, 2)
three_star.add_edge(1, 3)

three_path = nx.Graph()
three_path.add_edge(0, 1)
three_path.add_edge(1, 2)
three_path.add_edge(2, 3)

tailed_triangle = nx.Graph()
tailed_triangle.add_edge(0, 1)
tailed_triangle.add_edge(1, 2)
tailed_triangle.add_edge(0, 2)
tailed_triangle.add_edge(2, 3)

four_cycle = nx.Graph()
four_cycle.add_edge(0, 1)
four_cycle.add_edge(1, 2)
four_cycle.add_edge(2, 3)
four_cycle.add_edge(3, 0)

chordal_four_cycle = nx.Graph()
chordal_four_cycle.add_edge(0, 1)
chordal_four_cycle.add_edge(1, 2)
chordal_four_cycle.add_edge(0, 2)
chordal_four_cycle.add_edge(2, 3)
chordal_four_cycle.add_edge(3, 0)

four_clique = nx.Graph()
four_clique.add_edge(0, 1)
four_clique.add_edge(1, 2)
four_clique.add_edge(0, 2)
four_clique.add_edge(2, 3)
four_clique.add_edge(3, 1)
four_clique.add_edge(3, 0)

motifs = [three_path, tailed_triangle, four_cycle, chordal_four_cycle, four_clique]
motifs_cycle = [four_cycle, chordal_four_cycle, four_clique]
