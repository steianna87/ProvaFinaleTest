import networkx as nx
from matplotlib import pyplot as plt

from genera_spanning_tree import Istanza
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
    '''risultato1 = multi_robot_model(path='istanze_algoritmi/minimum/9x9/9x9_1-100_q=2 (3).txt', verbose=1)
    risultato2 = multi_robot_model(path='istanze/9x9/9x9_1-100_q=2 (3).txt', verbose=1)
    risultato3 = multi_robot_model(path='istanze/9x9/9x9_1-100_q=2 (3).txt', verbose=1)
    risultato4 = multi_robot_model(path='istanze/9x9/9x9_1-100_q=2 (3).txt', verbose=1)'''
    risultato_fake = Risultato(nx.Graph(), '', 0, 0, '', 0)
    ist = Istanza(path_grafo='istanze/9x9/9x9_1-100_q=2 (1).txt', grid_graph=True)
    risultato1 = Risultato(ist.grafo, '', 0, 0, '', 0)
    risultato2 = Risultato(ist.genera_AdditiveST()[0], '', 0, 0, '', 0)

    disegna_risultati([risultato1, risultato2], grid_graph=True)

    '''risultatE = multi_robot_model(path='istanze/Ventresca/ErdosRenyi_n235_1-100_q=2.txt', verbose=1)
    disegna_risultati([risultatE])'''

    ''' Gurobi Optimizer version 11.0.1 build v11.0.1rc0 (win64 - Windows 11.0 (22631.2))

        CPU model: Intel(R) Core(TM) i7-8565U CPU @ 1.80GHz, instruction set [SSE2|AVX|AVX2]
        Thread count: 4 physical cores, 8 logical processors, using up to 8 threads '''