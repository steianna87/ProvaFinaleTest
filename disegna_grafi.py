import networkx as nx
from matplotlib import pyplot as plt

from test import Risultato


def disegna(risultati: list[Risultato]):
    num_risultati = len(risultati)
    delta_x = 0
    delta_y = 0
    if num_risultati == 2 or num_risultati == 4:
        delta_x = 10
    if num_risultati == 3 or num_risultati == 4:
        delta_y = 10
    for risultato in risultati:
        num_nodes = len(risultato.grafo.nodes)
        num_cols = int(num_nodes ** 0.5)
        num_rows = (num_nodes + num_cols - 1) // num_cols
        pos = {}
        for i, node in enumerate(risultato.grafo.nodes):
            row = i // num_cols + delta_y
            col = i % num_cols + delta_x
            pos[node] = (col, -row)

        colori_edge = [edge[2]['color'] for edge in risultato.grafo.edges.data()]
        colori_node = [node[1]['color'] for node in risultato.grafo.nodes.data()]

        nx.draw(risultato.grafo, with_labels=True, pos=pos, edge_color=colori_edge, node_color=colori_node)

    plt.show()