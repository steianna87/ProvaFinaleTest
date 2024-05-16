import copy
from math import sqrt
from time import time

import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp
import random

import disegna_grafi
from test import multi_robot_model


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
        self.__nome_istanza = self.__path_grafo.split("/")[-1][:-4]
        self.__n = self.leggiIstanza(path_grafo)[0]
        self.__q = self.leggiIstanza(path_grafo)[1]
        self.listaPesi = self.leggiIstanza(path_grafo)[2]
        self.N = self.leggiIstanza(path_grafo)[3]
        self.grafo = self.inizializza_Grafo()

        self.soluzione = nx.Graph()
        self._subset = {}
        self._fOb = 1e16
        self._best_lb = 0
        self._elapsed_time = 0

    def risolvi(self):
        self.soluzione = self.inizializza_Grafo()
        self.soluzione.clear_edges()
        parziale = {}
        for s in range(2 * self.__q):
            if s < self.__q:
                parziale[s] = {'lista': [], 'Tot set': 0}
        self._best_lb = self.calcola_best_lb()

        t1 = time()
        self.ricorsione(parziale, 0)
        t2 = time()
        self._elapsed_time = t2 - t1

        colore_set = {0: 'red', 1: 'blue', 2: 'black', 3: 'green', 4: 'purple', 5: 'pink', 6: 'yellow'}
        for s in range(self.__q):
            for i in self._subset[s]['lista']:
                self.soluzione.nodes.data()[i]['color'] = colore_set[s]
            for nodo in self._subset[s]['lista']:
                for vicino in self.N[nodo]:
                    if vicino in self._subset[s]['lista']:
                        self.soluzione.add_edge(nodo, vicino, color=colore_set[s])

    def filtro(self, nodo, parziale_s_lista):
        if len(parziale_s_lista) == 0:
            return True
        vicini = self.N[nodo]
        for vicino in vicini:
            if vicino in parziale_s_lista:
                return True
        return False

    def get_max(self, parziale):
        return max(parziale[s]['Tot set'] for s in range(self.__q))

    def calcola_len(self, parziale):
        lunghezza = 0
        for s in range(self.__q):
            lunghezza += len(parziale[s]['lista'])
        return lunghezza

    def calcola_best_lb(self):
        return 1940             # per calcolare il best lb si potrebbe sfruttare il calcolo
                                # con il problema rilassato che utilizza già gurobi

    def ricorsione(self, parziale, pos):
        if self.calcola_len(parziale) != pos:
            return
        if self.get_max(parziale) > self._fOb:
            return
        if self.get_max(parziale) > self._best_lb:
            return

        if self._fOb == self._best_lb:
            return

        if pos == self.__n:
            print(parziale)
            if self.get_max(parziale) < self._fOb:
                self._fOb = self.get_max(parziale)
                self._subset = copy.deepcopy(parziale)
                # print(parziale)
        else:
            for nodo in range(pos, self.__n):
                pos += 1
                for s in range(self.__q):
                    if self.filtro(nodo, parziale[s]['lista']):
                        parziale[s]['lista'].append(nodo)
                        parziale[s]['Tot set'] += self.listaPesi[nodo]
                        self.ricorsione(parziale, pos)
                        parziale[s]['lista'].pop()
                        parziale[s]['Tot set'] -= self.listaPesi[nodo]

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
                break
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
            path = f'istanze_algoritmi/{tipo_algoritmo}/Ventresca/{self.__nome_istanza}.txt'

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
                self.grafo.add_weighted_edges_from([(nodo, vicino, peso_nodo + peso_vicino)], weight='weight')

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
    path = 'istanze/Ventresca/ForestFire_n250_1-100_q=2.txt'
    g = Istanza(path, grid_graph=False)
    rST, pathR = g.genera_RandomST()
    aST, pathA = g.genera_AdditiveST()
    mST, pathM = g.genera_MinimumST()

    if nx.is_connected(g.grafo):
        print('CONNESSO')
    else:
        print('NON CONNESSO')

    # risultato = multi_robot_model(pathM, 1)

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
        col = i % num_cols + 15
        pos2[node] = (col, -row)
    pos3 = {}
    for i, node in enumerate(g.grafo.nodes):
        row = i // num_cols + 15
        col = i % num_cols
        pos3[node] = (col, -row)
    pos4 = {}
    for i, node in enumerate(g.grafo.nodes):
        row = i // num_cols + 15
        col = i % num_cols + 15
        pos4[node] = (col, -row)

    '''nx.draw(g.grafo, with_labels=True, node_size=100)
    plt.show()
    nx.draw(g.grafo, with_labels=True, edge_color='red', node_size=100)
    plt.show()
    nx.draw(aST, with_labels=True, edge_color='green', node_size=100)
    plt.show()
    nx.draw(mST, with_labels=True, edge_color='blue', node_size=100)
    plt.show()'''
    print()
    '''print(g)
    print(pathR)
    print(rST.edges.data())
    print(aST.edges.data())
    print(mST.edges.data())'''
