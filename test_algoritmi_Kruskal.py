from time import time

from networkx import Graph

from test import multi_robot_model, Risultato
from genera_spanning_tree import Istanza
from disegna_grafi import disegna

# Approccio con formazione di spanning tree grazie all'algoritmo di Kruskal e Random
path = "istanze/9x9/9x9_1-100_q=2 (1).txt"

istanza = Istanza(path, grid_graph=True)

# Algoritmo Random
risultati_random = []
t1 = time()
durata = 0.0
best_risultato = Risultato(Graph(), 'Nessun risultato', 1e16, 0, 'NO_SOLUTION_FOUND', 0)
tentativo_migliore = 0
while durata < 10:
    rST, path_random = istanza.genera_RandomST()
    risultato_rST = multi_robot_model(path_random, 0)
    risultati_random.append(risultato_rST)
    t2 = time()
    durata = t2 - t1
    if risultato_rST.fun_obiettivo < best_risultato.fun_obiettivo:
        best_risultato = risultato_rST
        best_risultato.time = durata
        best_risultato.grafo = rST
        tentativo_migliore = len(risultati_random)

tentativi = len(risultati_random)
istanza.scriviIstanza(best_risultato.grafo, 'random', True)

# Algoritmo Additive
aST, path_additive = istanza.genera_AdditiveST()
risultato_aST = multi_robot_model(path_additive, 1)

# Algoritmo Minimum
mST, path_minimum = istanza.genera_MinimumST()
risultato_mST = multi_robot_model(path_minimum, 1)

disegna([best_risultato, risultato_aST, risultato_mST])

print()
print(f'************* RISULTATI *************\n'
      f'Random (tentativi: {tentativi} migliore: {tentativo_migliore}): {best_risultato}\n'
      f'Additive: {risultato_aST}\n'
      f'Minimum: {risultato_mST}\n')
'''
path_kruskal = "istanze/Ventresca/ErdosRenyi_n466_1-100_q=2.txt"
nomeIstanza, risultato = multi_robot_model(path_kruskal)
'''
