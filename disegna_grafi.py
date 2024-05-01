import networkx as nx
from matplotlib import pyplot as plt

from test import Risultato, multi_robot_model


def disegna_risultati(risultati: list[Risultato], grid_graph: bool = False):
    if len(risultati) > 4:
        print('TROPPI RISULTATI INSIEME, MASSIMO 4 CONTEMPORANEAMENTE')

    if grid_graph:
        for risultato in risultati:
            if nx.is_empty(risultato.grafo):
                print('GRAFO VUOTO')
                pass
            num_risultato = risultati.index(risultato)
            delta_x = 0
            delta_y = 0
            if num_risultato == 1 or num_risultato == 3:
                delta_x = 15
            if num_risultato == 2 or num_risultato == 3:
                delta_y = 15

            num_nodes = len(risultato.grafo.nodes)
            num_cols = int(num_nodes ** 0.5)

            pos = {}
            for i, node in enumerate(risultato.grafo.nodes):
                row = i // num_cols + delta_y
                col = i % num_cols + delta_x
                pos[node] = (col, -row)

            colori_edge = [edge[2]['color'] for edge in risultato.grafo.edges.data()]
            colori_node = [node[1]['color'] for node in risultato.grafo.nodes.data()]

            nx.draw(risultato.grafo, with_labels=True, pos=pos, edge_color=colori_edge, node_color=colori_node,
                    node_size=100)
    else:
        for risultato in risultati:
            if nx.is_empty(risultato.grafo):
                print('GRAFO VUOTO')
                pass

            colori_edge = [edge[2]['color'] for edge in risultato.grafo.edges.data()]
            colori_node = [node[1]['color'] for node in risultato.grafo.nodes.data()]

            nx.draw(risultato.grafo, with_labels=True, edge_color=colori_edge, node_color=colori_node,
                    node_size=100)

    plt.show()


if __name__ == '__main__':
    risultato1 = multi_robot_model(path='istanze_algoritmi/minimum/9x9/9x9_1-100_q=2 (3).txt', verbose=1)
    risultato2 = multi_robot_model(path='istanze/9x9/9x9_1-100_q=2 (3).txt', verbose=1)
    risultato3 = multi_robot_model(path='istanze/9x9/9x9_1-100_q=2 (3).txt', verbose=1)
    risultato4 = multi_robot_model(path='istanze/9x9/9x9_1-100_q=2 (3).txt', verbose=1)
    risultato_fake = Risultato(nx.Graph(), '', 0, 0, '', 0)

    disegna_risultati([risultato_fake, risultato2, risultato3, risultato4])

    '''risultatE = multi_robot_model(path='istanze/Ventresca/ErdosRenyi_n235_1-100_q=2.txt', verbose=1)
    disegna_risultati([risultatE])'''
