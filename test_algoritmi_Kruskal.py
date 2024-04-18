from test import multi_robot_model

# Approccio con formazione di spanning tree grazie all'algoritmo di Kruskal
path = "istanze/9x9/9x9_1-100_q=2 (1).txt"

# Algoritmo Random



path_kruskal = "istanze/Ventresca/ErdosRenyi_n466_1-100_q=2.txt"
nomeIstanza, risultato = multi_robot_model(path_kruskal)
