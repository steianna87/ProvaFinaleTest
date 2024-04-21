from math import sqrt

import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp
import random


def replace_chars(stringa: str):
    out_str = ''
    for char in stringa:
        if "[,]".__contains__(char):
            pass
        else:
            out_str += char
    return out_str


class Istanza:
    def __init__(self, path_grafo, grid_graph: bool = False):
        self.__path_grafo = path_grafo
        self.__grid_graph = grid_graph
        self.__n = self.leggiIstanza(path_grafo)[0]
        self.__q = self.leggiIstanza(path_grafo)[1]
        self.listaPesi = self.leggiIstanza(path_grafo)[2]
        self.N = self.leggiIstanza(path_grafo)[3]
        self.grafo = self.inizializza_Grafo()

    def leggiIstanza(self, file):
        with open(file, 'r', encoding='utf-8') as istanza:
            riga1 = istanza.readline().strip().split(' ')
            n = int(riga1[0])
            q = int(riga1[1])
            istanza.readline()

            listaStanze = [int(w) for w in istanza.readline().strip().split(' ')]
            if n != len(listaStanze):
                return n, q, [], [[]]
            N = [[] for i in range(n)]
            for righe in istanza:
                riga = righe.strip().split(':')
                N[int(riga[0])] = [int(i) for i in riga[1].strip().split(' ')]

        return n, q, listaStanze, N

    def scriviIstanza(self, grafo, tipo_algoritmo, grid_graph: bool):
        global max_peso, path
        numFile = self.__path_grafo[-6]

        for peso in self.listaPesi:
            if peso > 100:
                max_peso = 500
            else:
                max_peso = 100
        node_id = {}

        for i, node in enumerate(sorted(grafo.nodes())):
            node_id[node] = i

        risultato = ''

        risultato += f'{self.__n} {self.__q}\n'
        risultato += '\n'
        risultato += f'{self.listaPesi}'
        # Stampa dell'associazione nodo - numero e dei vicini di ciascun nodo
        for node, number in sorted(node_id.items(), key=lambda x: x[1]):
            neighbors = sorted(grafo.neighbors(node))
            risultato += '\n'
            risultato += f"{number}: {[node_id[n] for n in neighbors]}"

        # print(risultato)
        risultato = replace_chars(risultato)

        if grid_graph:
            n = int(sqrt(self.__n))
            path = f'istanze_algoritmi/{tipo_algoritmo}/{n}x{n}/{n}x{n}_1-{max_peso}_q={self.__q} ({numFile}).txt'
        else:
            path = f'istanze_algoritmi/{tipo_algoritmo}/Ventresca/n{self.__n}_1-{max_peso}_q={self.__q} ({numFile}).txt'

        with open(path, 'w', encoding='utf-8') as file:
            file.write(risultato)
        return path

    def inizializza_Grafo(self):
        grafo = nx.Graph()
        for nodo, peso in enumerate(self.listaPesi):
            grafo.add_node(nodo, weight=peso)
        for nodo in range(len(self.N)):
            for vicino in self.N[nodo]:
                grafo.add_edge(nodo, vicino)
        print(grafo)
        return grafo

    def genera_RandomST(self):
        ST = nx.random_spanning_tree(self.grafo)
        path = self.scriviIstanza(ST, 'random', grid_graph=self.__grid_graph)
        return ST, path

    def genera_AdditiveST(self):
        self.grafo.clear_edges()

        for nodo in range(len(self.N)):
            peso_nodo = self.listaPesi[nodo]
            for vicino in self.N[nodo]:
                peso_vicino = self.listaPesi[vicino]
                self.grafo.add_weighted_edges_from([(nodo, vicino, peso_nodo+peso_vicino)], weight='weight')

        ST = nx.minimum_spanning_tree(self.grafo, algorithm='kruskal', weight='weight')
        path = self.scriviIstanza(ST, 'additive', grid_graph=self.__grid_graph)
        return ST, path

    def genera_MinimumST(self):
        self.grafo.clear_edges()

        for nodo in range(len(self.N)):
            peso_nodo = self.listaPesi[nodo]
            for vicino in self.N[nodo]:
                peso_vicino = self.listaPesi[vicino]
                self.grafo.add_weighted_edges_from([(nodo, vicino, min(peso_nodo, peso_vicino))], weight='weight')

        ST = nx.minimum_spanning_tree(self.grafo, algorithm='kruskal', weight='weight')
        path = self.scriviIstanza(ST, 'minimum', grid_graph=self.__grid_graph)
        return ST, path

    def __str__(self):
        return (f'path: {self.__path_grafo}\n'
                f'nodi: {self.grafo.nodes}\n'
                f'spigoli: {self.grafo.edges}\n'
                f'path ST: {self.genera_RandomST()[1]}\n'
                f'spanning tree: {self.genera_MinimumST()[0].edges.data()}')


if __name__ == '__main__':
    g = Istanza('istanze/9x9/9x9_1-100_q=2 (1).txt', grid_graph=True)
    rST, pathR = g.genera_RandomST()
    aST = g.genera_AdditiveST()[0]
    mST = g.genera_MinimumST()[0]

    num_nodes = len(g.grafo.nodes)
    num_cols = int(num_nodes ** 0.5)
    num_rows = (num_nodes + num_cols - 1) // num_cols
    pos = {}
    for i, node in enumerate(g.grafo.nodes):
        row = i // num_cols
        col = i % num_cols
        pos[node] = (col, -row)
    pos2 = {}
    for i, node in enumerate(g.grafo.nodes):
        row = i // num_cols
        col = i % num_cols + 10
        pos2[node] = (col, -row)
    pos3 = {}
    for i, node in enumerate(g.grafo.nodes):
        row = i // num_cols + 10
        col = i % num_cols
        pos3[node] = (col, -row)
    pos4 = {}
    for i, node in enumerate(g.grafo.nodes):
        row = i // num_cols + 10
        col = i % num_cols + 10
        pos4[node] = (col, -row)

    nx.draw(g.grafo, with_labels=True, pos=pos)
    nx.draw(rST, with_labels=True, pos=pos2, edge_color='red')
    nx.draw(aST, with_labels=True, pos=pos3, edge_color='green')
    nx.draw(mST, with_labels=True, pos=pos4, edge_color='blue')

    plt.show()
    print()
    print(g)
    print(pathR)
