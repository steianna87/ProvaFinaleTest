from mip import *

stanze = [[10, 11, 1],
          [5, 5, 11],
          [5, 5, 10]]

listaStanze = [j for i in range(len(stanze)) for j in stanze[i]]
#print(listaStanze)

n = len(listaStanze)
# spigoli[i][j] = 1 se esiste lo spigolo tra i e j, 0 altrimenti
spigoli = [[] for i in range(n)]

spigoli[0] = [2, 4]
spigoli[1] = [1, 3, 5]
spigoli[2] = [2, 6]
spigoli[3] = [1, 4, 7]
spigoli[4] = [2, 4, 6, 8]
spigoli[5] = [3, 5, 9]
spigoli[6] = [4, 8]
spigoli[7] = [5, 7, 9]
spigoli[8] = [6, 8]




for riga, listaRiga in enumerate(spigoli):
    print(listaRiga)
print()


m = Model('multiRobot')


# NODE LABELING

# numero stanze  n = len(listaStanze)
n = 9
# numero robot
q = 3
# variabili per etichettare (label) un nodo i al robot s
x = [[m.add_var('x({})({})'.format(i+1, s+1), var_type=BINARY) for s in range(q)] for i in range(n)]

# funzione obiettivo
t = m.add_var(name='setSlower')
for s in range(q):
    m += xsum(x[i][s] * listaStanze[i] for i in range(n)) <= t              # (3)

m.objective = minimize(t)                                                   # (2)

# ogni stanza dev'essere assegnata ad un solo set (robot)
for i in range(n):
    m += xsum(x[i][s] for s in range(q)) == 1                               # (4)


# FLOW MODEL

# Flow reception
# variabile per etichettatre (label) il nodo reception
r = [[m.add_var('r({})({})'.format(i, s), var_type=BINARY) for s in range(1, q+1)] for i in range(1, n+1)]
for i in range(n):
    for s in range(q):
        m += r[i][s] <= x[i][s]                                             # (5)
# un solo nodo reception per set
for s in range(q):
    m += xsum(r[i][s] for i in range(n)) == 1                               # (6)
# selezionare come reception il nodo x(i)(s) = 1 con l'indice i più piccolo per velocizzare i calcoli
for i in range(n):
    for s in range(q):
        m += n * r[i][s] <= (n + 1 - xsum(x[j][s] for j in range(i+1)))     # (7)

# F flow trasportato dal nodo i al nodo j
F = [[m.add_var('F({})({})'.format(i, j+1), var_type=INTEGER) for j in range(n)] for i in range(n+1)]
# carica delle reception: nodo sorgente 0 fittizio (dummy) da cui parte il flow
for i in range(n):
    m += F[0][i] <= n * xsum(r[i][s] for s in range(q))                     # (8) la sommatoria è 1 se il nodo i è reception, 0 altrimenti


# Flow consumption
'''
def nodiVicini(spigoli, nodo):
    N = []
    for i in range(len(spigoli)):
        if spigoli[nodo][i] == 1:
            N.append(i)
    #N.append(0)
    return N
'''

# flow totale
m += xsum(F[0][i] for i in range(n)) == n                                   # (9)

# ogni nodo consuma un'unità di flow ogni volta che il flow passa in esso (eccetto il nodo sorgente 0)
for i in range(n):
    #N = nodiVicini(spigoli, i)
    N = spigoli[i]
    m += xsum(F[j][i] for j in N) - xsum(F[i+1][k-1] for k in N) + F[0][i] == 1       # (10)

# Flow transportation
# variabilie y(i)(j)(s) = 1 se il nodo i e j sono entrambi etichettati (labeled) al set s
y = [[[m.add_var('y({})({})({})'.format(i, j, s), var_type=BINARY) for s in range(1, q+1)] for j in range(1, n+1)] for i in range(1, n+1)]
for i in range(n):
    for j in range(n):
        m += F[i+1][j] <= n * xsum(y[i][j][s] for s in range(q))            # (11)
        # vincoli per linearizzare y(i)(j)(s) = x(i)(s) * x(j)(s)
        for s in range(q):
            m += y[i][j][s] <= x[i][s]                                      # (12)
            m += y[i][j][s] <= x[j][s]                                      # (13)
            m += y[i][j][s] >= 0                                            # (14)
            m += y[i][j][s] >= x[i][s] + x[j][s] - 1                        # (15)

def stampaSoluzione():
    soluzione = []
    if m.num_solutions:
        for i in range(n):
            for s in range(q):
                if float(r[i][s].x) >= 0.99:
                    soluzione.append('r' + (s+1).__str__())
                elif float(x[i][s].x) >= 0.99:
                    soluzione.append(' ' + (s+1).__str__())

    indiciAcapo = []
    indice = 0
    indiciAcapo.append(indice)
    for riga in stanze:
        indice += len(riga)
        indiciAcapo.append(indice)

    elenco = ''
    for num, val in enumerate(soluzione):
        if num in indiciAcapo:
            elenco += '\n'
        elenco += val + ' '
    print()
    print(elenco)
    print()


m.optimize(max_seconds=10)
m.write('bozza.lp')
stampaSoluzione()
