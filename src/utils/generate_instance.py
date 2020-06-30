from random import randint
import sys

n = int(sys.argv[1]) # Número de cidades
MAX_CUSTO = int(sys.argv[2]) # Custo máximo

filename = '../instance_' + str(n) + '.txt'
arq = open(filename, 'w')
arq.write(str(n)+'\n')

M = []

def geraVetor(z_index):
  v = []
  for i in range(0,n):
    if i == z_index:
      v.append(0)
    else:
      rd = randint(1,MAX_CUSTO)
      v.append(rd)
  return v

for i in range(0,n):
  line = geraVetor(i)
  M.append(line)

for lin in range(0,n):
  for col in range(0,n):
    if lin > col:
      M[lin][col] = M[col][lin]

for lin in range(0,n):
  for col in range(0,n):
    if col == n-1:
      arq.write(str(M[lin][col]))
    else:
      arq.write(str(M[lin][col]) + ' ')
  arq.write('\n')
arq.close()