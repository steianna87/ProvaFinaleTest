import matplotlib.pyplot as plt
import networkx as nx

import disegna_grafi
import test
from genera_spanning_tree import Istanza
import scipy as sp

"istanze/9x9/9x9_1-100_q=2 (1).txt"

risultato = test.multi_robot_model("istanza_3x3_1-100_q=2.txt", 0)
ist = Istanza(path_grafo="istanze/Ventresca/WattsStrogatz_n250_1-500_q=4.txt", grid_graph=True)
ist.risolvi()
print()
print(risultato)
print()
print(ist._subset)
print(ist._fOb)
print(ist._elapsed_time)

num_nodes = len(ist.soluzione.nodes)
num_cols = int(num_nodes ** 0.5)
pos = {}
for i, node in enumerate(ist.soluzione.nodes):
    row = i // num_cols
    col = i % num_cols
    pos[node] = (col, -row)

disegna_grafi.disegna_risultati([risultato], grid_graph=True)
plt.show()
try:
    colori_edge = [edge[2]['color'] for edge in ist.soluzione.edges.data()]
    colori_node = [node[1]['color'] for node in ist.soluzione.nodes.data()]
    nx.draw(ist.soluzione, node_color=colori_node, edge_color=colori_edge, with_labels=True)
except KeyError:
    print('NESSUNA SOLUZIONE TROVATA TRAMITE RICORSIONE')
plt.show()
