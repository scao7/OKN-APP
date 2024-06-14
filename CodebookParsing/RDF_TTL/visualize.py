import rdflib
import networkx as nx
import matplotlib.pyplot as plt

# Load the TTL file into an RDF graph
g = rdflib.Graph()
g.parse('example.ttl', format='turtle')

# Initialize a NetworkX graph
G = nx.Graph()

# Iterate over triples in the RDF graph and add nodes and edges to NetworkX graph
for subj, pred, obj in g:
    G.add_node(subj)
    G.add_node(obj)
    G.add_edge(subj, obj, label=pred)

# Draw the NetworkX graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)  # Positions for all nodes
nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue')
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edge_color='grey')
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

plt.title('RDF Graph Visualization')
plt.axis('off')
plt.show()
