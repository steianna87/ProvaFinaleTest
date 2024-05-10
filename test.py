from dataclasses import dataclass
from time import *

import matplotlib.pyplot as plt
import networkx as nx
from mip import *
from networkx import Graph


@dataclass
class Risultato:
    grafo: Graph
    nome_istanza: str
    fun_obiettivo: float
    time: float
    stato_soluzione: str
    best_lb: float

    def __str__(self):
        return (f'| Nome Istanza: {self.nome_istanza} | Fun. Obiettivo: {self.fun_obiettivo} | Time: {self.time} | '
                f'Stato soluzione: {self.stato_soluzione} | Best lb: {self.best_lb} |')


def multi_robot_model(path: str, verbose: int):
    def contaSPigoli(N):
        num = 0
        for nodo in N:
            for vicini in nodo:
                num += 1
        return num//2


    def leggiIstanza(file):
        with open(file, 'r', encoding='utf-8') as istanza:
            riga1 = istanza.readline().strip().split(' ')
            n = int(riga1[0])
            q = int(riga1[1])
            istanza.readline()

            listaStanze = [int(w) for w in istanza.readline().strip().split(' ')]
            if n != len(listaStanze):
                return 0, 0, [], [[]]
            N = [[] for i in range(n)]
            for righe in istanza:
                riga = righe.strip().split(':')
                N[int(riga[0])] = [int(i) for i in riga[1].strip().split(' ')]

        print(f'{n} stanze, {len(listaStanze)} pesi\n'
              f'{q} robot\n'
              f'{contaSPigoli(N)} spigoli\n')
        return n, q, listaStanze, N


    #path = "istanze/Ventresca/ErdosRenyi_n466_1-100_q=2.txt"
    n, q, listaStanze, N = leggiIstanza(path)

    m = Model('multiRobot')
    m.max_mip_gap = 0

    # NODE LABELING

    # numero stanze  n = len(listaStanze)
    # n = len(listaStanze)
    # numero robot
    # q = 2
    # variabili per etichettare (label) un nodo i al robot s
    x = [[m.add_var('x({})({})'.format(i + 1, s + 1), var_type=BINARY) for s in range(q)] for i in range(n)]

    # funzione obiettivo
    t = m.add_var(name='setSlower')
    for s in range(q):
        m += xsum(x[i][s] * listaStanze[i] for i in range(n)) <= t  # (3)

    m.objective = minimize(t)  # (2)

    # ogni stanza dev'essere assegnata ad un solo set (robot)
    for i in range(n):
        m += xsum(x[i][s] for s in range(q)) == 1  # (4)

    # FLOW MODEL

    # Flow reception
    # variabile per etichettatre (label) il nodo reception
    r = [[m.add_var('r({})({})'.format(i + 1, s + 1), var_type=BINARY) for s in range(q)] for i in range(n)]
    for i in range(n):
        for s in range(q):
            m += r[i][s] <= x[i][s]  # (5)
    # un solo nodo reception per set
    for s in range(q):
        m += xsum(r[i][s] for i in range(n)) == 1  # (6)
    # selezionare come reception il nodo x(i)(s) = 1 con l'indice i più piccolo per velocizzare i calcoli
    for i in range(n):
        for s in range(q):
            m += n * r[i][s] <= (n + 1 - xsum(x[j][s] for j in range(i + 1)))  # (7)

    # F flow trasportato dal nodo i al nodo j
    F = [[m.add_var('F({})({})'.format(i + 1, j + 1), var_type=INTEGER) if i != j else None for j in range(n)] for i in range(n + 1)]
    # carica delle reception: nodo sorgente 0 fittizio (dummy) da cui parte il flow
    for i in range(n):
        m += F[n][i] <= n * xsum(r[i][s] for s in range(q))  # (8) la sommatoria è 1 se il nodo i è reception, 0 altrimenti

    # Flow consumption

    # flow totale
    m += xsum(F[n][i] for i in range(n)) == n  # (9)

    # ogni nodo consuma un'unità di flow ogni volta che il flow passa in esso (eccetto il nodo sorgente 0)
    for i in range(n):
        # N = nodiVicini(spigoli, i)
        # N = N[i]
        m += xsum(F[j][i] for j in N[i]) - xsum(F[i][k] for k in N[i]) + F[n][i] == 1  # (10)

    # Flow transportation
    # variabilie y(i)(j)(s) = 1 se il nodo i e j sono entrambi etichettati (labeled) al set s
    y = [[[m.add_var('y({})({})({})'.format(i + 1, j + 1, s + 1), var_type=BINARY) if i != j else None for s in range(q)]
          for j in range(n)] for i in range(n)]
    #nodiAccoppiati = []
    for i in range(n):
        for j in N[i]:
            m += F[i][j] <= n * xsum(y[i][j][s] for s in range(q))  # (11)
            #if not nodiAccoppiati.__contains__({i, j}):
                #nodiAccoppiati.append({i, j})
            # vincoli per linearizzare y(i)(j)(s) = x(i)(s) * x(j)(s)
            for s in range(q):
                m += y[i][j][s] <= x[i][s]  # (12)
                m += y[i][j][s] <= x[j][s]  # (13)
                m += y[i][j][s] >= 0  # (14)
                m += y[i][j][s] >= x[i][s] + x[j][s] - 1  # (15)
                    #m += y[i][j][s] == y[j][i][s]

    m.store_search_progress_log = True
    m.verbose = verbose
    status = m.optimize(max_seconds=200)
    dati = m.search_progress_log.log
    nomeIstanza = f'{path.split("/")[-1][:-4]}'          # GridGraph_

    lb = dati[-1][1][0]
    print(lb)
    print(dati[-1])
    for dato in dati:
        if dato[1][0] < lb and dati.index(dato) > 10:
            lb = dato[1][0]
    print(lb)


    # Grafo della soluzione
    soluzione = nx.Graph()

    colore_set = {0: 'red', 1: 'blue', 2: 'black', 3: 'green', 4: 'purple', 5: 'pink', 6: 'yellow'}

    if m.num_solutions:
        for i in range(n):
            for s in range(q):
                if float(x[i][s].x) > 0.99:
                    soluzione.add_node(i, set=s, color=colore_set[s])

        for s in range(q):
            for i in range(n):
                for j in range(n):
                    if F[i][j] is not None and int(F[i][j].x) > 0 and y[i][j][s] is not None and float(y[i][j][s].x) > 0.99:
                        soluzione.add_edge(i, j, color=colore_set[s])

    print()
    #risultato = (f'| Nome Istanza: {nomeIstanza} | Fun. Obiettivo: {m.objective_value} | Time: {dati[-1][0]} | Stato '
    #             f'soluzione: {status.__str__().split(".")[1]} | Best lb: {lb} |')
    risultato = Risultato(soluzione, nomeIstanza, float(m.objective), dati[-1][0], status.__str__().split(".")[1], lb)
    #print(risultato)
    return risultato

if __name__ == '__main__':
    risultato = multi_robot_model(path="istanze/9x9/9x9_1-100_q=2 (1).txt", verbose=1)
    print(risultato)

    num_nodes = len(risultato.grafo.nodes)
    num_cols = int(num_nodes ** 0.5)
    num_rows = (num_nodes + num_cols - 1) // num_cols
    pos = {}
    for i, node in enumerate(risultato.grafo.nodes):
        row = i // num_cols
        col = i % num_cols
        pos[node] = (col, -row)

    colore_set = {0: 'red', 1: 'blue', 2: 'black', 3: 'green', 4: 'purple', 5: 'pink', 6: 'yellow'}
    colori_edge = [edge[2]['color'] for edge in risultato.grafo.edges.data()]
    colori_node = [node[1]['color'] for node in risultato.grafo.nodes.data()]

    nx.draw(risultato.grafo, with_labels=True, pos=pos, edge_color=colori_edge, node_color=colori_node)

    plt.show()

    '''with open('risultati_test.txt', 'r+', encoding='utf-8') as file:
        numRighe = len(file.readlines())
        file.seek(0)
        for i in range(numRighe-1):
            file.readline()
        ultimaRiga = file.readline()
        cella = ultimaRiga.strip().split('|')[1]
        nome = cella.strip().split(':')[1].lstrip()
        if nome != nomeIstanza or numRighe == 0:
            file.write(risultato+'\n')'''


