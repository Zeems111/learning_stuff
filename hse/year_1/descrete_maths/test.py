import networkx as nx
import matplotlib as mp
'''
mygraph = nx.Graph()
#mygraph = nx.DiGraph()
mygraph.add_node('X')
mygraph.add_edge('A', 'B')
mygraph.add_edge('B', 'C')
mygraph.add_edge('A', 'C', weight=5)
mygraph.add_edge('D', 'B')
mygraph.add_edge('D', 'X')
nx.draw_networkx(mygraph)
# nx.draw_networkx(mygraph, with_labels=False)
mp.pyplot.savefig('mygraph.jpg')
av_clust = nx.average_clustering(mygraph)

print('av_clust:',av_clust)
if nx.is_connected(mygraph):
    eccentricity = nx.eccentricity(mygraph)
    print(eccentricity)

    diam = nx.diameter(mygraph)
    print('diametr:', diam)

if nx.has_path(mygraph, 'A','X'):
    print(nx.shortest_path(mygraph, 'A', 'X'))
else:
    print('Not connected')

print(*(nx.dfs_preorder_nodes(mygraph, source='C')))
'''

g = nx.read_edgelist('facebook_combined.txt')
g_edges = len(nx.edges(g))
g_vertices = len(g)
#g_av_clust = nx.average_clustering(g)
#print(round(g_av_clust, 3))
#print(nx.induced_subgraph(g, [0]))
#probability = 2 * g_edges/(g_vertices * (g_vertices-1))

#g2 = nx.erdos_renyi_graph(g_vertices, probability)
#print(g2)
#g2_av_clust = nx.average_clustering(g2)
#print(round(g2_av_clust, 3))
vs = [0, 107, 348, 414, 612, 686, 698, 1684, 1912, 3437, 3980]
vs = list(map(str, vs))
print(vs)
gs = []
for i in vs:
    print(i, len(nx.edges(g, i)))
    print(i, len(nx.ego_graph(g, i, radius=1)))
    print('-------------')
print(nx.edges(g, '612'))
#len(nx.ego_graph(vs))
#for i in nx.edges(g, vs):
   # print(i)

#nx.draw_networkx(g, with_labels=False)
#mp.pyplot.savefig('g.png')