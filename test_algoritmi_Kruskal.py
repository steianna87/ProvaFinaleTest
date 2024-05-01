from time import time

from networkx import Graph

from test import multi_robot_model, Risultato
from genera_spanning_tree import Istanza
from disegna_grafi import disegna_risultati

# Approccio con formazione di spanning tree grazie all'algoritmo di Kruskal e Random
path = "istanze/Ventresca/WattsStrogatz_n1000_1-100_q=2.txt"
grid_graph = False
istanza = Istanza(path, grid_graph=grid_graph)

# Modello Standard
#risultato_standard = multi_robot_model(path, 1)

# Algoritmo Random
risultati_random = []
t1 = time()
durata = 0.0
best_risultato = Risultato(Graph(), 'Nessun risultato', 1e16, 0, 'NO_SOLUTION_FOUND', 0)
tentativo_migliore = 0
while durata < 200:
    rST, path_random = istanza.genera_RandomST()
    risultato_rST = multi_robot_model(path_random, 1)
    risultati_random.append(risultato_rST)
    t2 = time()
    durata = t2 - t1
    print(f'durata: {durata}')
    if risultato_rST.fun_obiettivo < best_risultato.fun_obiettivo:
        best_risultato = risultato_rST
        best_risultato.time = durata
        tentativo_migliore = len(risultati_random)

tentativi = len(risultati_random)
istanza.scriviIstanza(best_risultato.grafo, 'random', grid_graph)

# Algoritmo Additive
aST, path_additive = istanza.genera_AdditiveST()
risultato_aST = multi_robot_model(path_additive, 1)

# Algoritmo Minimum
mST, path_minimum = istanza.genera_MinimumST()
risultato_mST = multi_robot_model(path_minimum, 1)

if grid_graph:
    disegna_risultati([best_risultato, risultato_aST, risultato_mST], grid_graph=grid_graph)
else:
    disegna_risultati([best_risultato])
    disegna_risultati([risultato_aST])
    disegna_risultati([risultato_mST])
    pass

print()
risultato = (f'************* RISULTATI: {path} *************\n'
             f'Random (tentativi: {tentativi} migliore: {tentativo_migliore}): {best_risultato}\n'
             f'Additive: {risultato_aST}\n'
             f'Minimum: {risultato_mST}\n')

with open('risultati_test_algoritmi_random-add-min.txt', 'r+', encoding='utf-8') as file:
    numRighe = len(file.readlines())
    if numRighe == 0:
        file.write(risultato)
    else:
        file.seek(0)
        for i in range(numRighe - 1):
            file.readline()
        ultimaRiga = file.readline()
        cella = ultimaRiga.strip().split('|')[1]
        nome = cella.strip().split(':')[1].lstrip()
        if nome != risultato_aST.nome_istanza:
            file.write(risultato)

print('******************************************************************************')
