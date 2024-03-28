import random
from mip import *

pesi = [random.randint(1, 100) for i in range(1500)]

risultato = ''
for i in pesi:
    if risultato != '':
        risultato += ' '
    risultato += i.__str__()
print(risultato)
'''
m = Model()
for i in range(4):
    for j in range(4):
        if i != j:
            x = m.add_var(name='x({})({})'.format(i, j))

print(m.var_by_name('x(1)(2)'))
'''

