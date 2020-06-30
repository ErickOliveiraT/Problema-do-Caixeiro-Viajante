from random import randint

n = 100

filename = 'instance_' + str(n) + '.txt'
arq = open(filename, 'w')
arq.write(str(n)+'\n')

for i in range(0,n):
  for j in range(0,n):
    if i == j:
      arq.write('0 ')
    else:
      rd = randint(0,100)
      arq.write(str(rd)+' ') 
  arq.write('\n')
arq.close()