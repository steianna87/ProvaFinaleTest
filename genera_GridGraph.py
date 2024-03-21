import networkx as nx
import random

n = 11               # RICORDA DI CAMBIARAE IL NUMERO DEL FILE NELLE () DEL PATH
q = 2
max_peso = 500

# Creazione del grafo
G = nx.grid_2d_graph(n, n)

# Assegnazione di un numero unico a ciascun nodo
node_id = {}
for i, node in enumerate(sorted(G.nodes())):
    node_id[node] = i

pesi = [random.randint(1, max_peso) for i in range(n * n)]

risultato = ''

risultato += f'{n * n} {q}\n'
risultato += '\n'
risultato += f'{pesi}'.replace('[', '').replace(']', '').replace(',', '')
# Stampa dell'associazione nodo - numero e dei vicini di ciascun nodo
for node, number in sorted(node_id.items(), key=lambda x: x[1]):
    neighbors = sorted(G.neighbors(node))
    risultato += '\n'
    risultato += f"{number}: {[node_id[n] for n in neighbors]}".replace('[', '').replace(']', '').replace(',', '')

print(risultato)

path = f'istanze/{n}x{n}/{n}x{n}_1-{max_peso}_q={q} (1).txt'
with open(path, 'w', encoding='utf-8') as file:
    file.write(risultato)
