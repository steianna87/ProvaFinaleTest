from disegna_grafi import disegna_risultati
from genera_spanning_tree import Istanza
from test import multi_robot_model

path1 = "istanze/9x9/9x9_1-100_q=2 (1).txt"
path2 = "istanze/12x12/12x12_1-100_q=5 (1).txt"
grid_graph = True


risultato1 = multi_robot_model(path=path1, verbose=1)
risultato2 = multi_robot_model(path=path2, verbose=1)
disegna_risultati([risultato1, risultato2], grid_graph=grid_graph)
