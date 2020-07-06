from random import randint
from time import time

#Config:
instance = open('../../instances/instance_10.txt', 'r') #Instância (pasta src/instances)
prob_mutacao = 0.05 #Probabilidade de mutação do algoritmo genético
max_deep = 2

def carregarMatriz(): #Lê uma matriz de adjacência
    n = int(instance.readline())
    data = instance.readlines()
    matriz = []
    for row in data:
        aux = []
        line = row.split('\t')
        for num in line:
            aux.append(int(num))
        matriz.append(aux)
    instance.close()
    return matriz

def imprimirMatriz(m): #Imprime uma matriz de adjacência
    for lin in m:
        for col in lin:
            print(col, end='\t')
        print('')

def resolver_guloso(m): #Calcula uma caminho pelo método do vizinho mais próximo
    caminho = [0] #Visita cidade 0 primeiro
    visitados = [0] #Vetor de cidades já visitadas
    last = 0 #Última cidade visitada
    while len(caminho) < len(m[0]):
        menor = 999999 #Menor custo encontrado
        for i in range(0, len(m[last])):
            if m[last][i] > 0 and m[last][i] < menor:
                if i not in visitados: #Cidade ainda não visitada
                    menor = m[last][i]
                    selecionado = i
        visitados.append(selecionado)
        caminho.append(selecionado)
        last = selecionado
    caminho.append(0)
    return caminho

def calc_custo(caminho, m):
    custo = 0
    for i in range(0, len(caminho)-1):
        custo += m[caminho[i]][caminho[i+1]]
    return custo

def swap_random(caminho):
    i1 = randint(1, len(caminho)-1)
    i2 = randint(1, len(caminho)-1)
    return swap(caminho, i1, i2)

def random_choice():
    rd = randint(1,100)
    if rd <= 5:
        return True
    return False

def swap(caminho, i1, i2):
    temp = caminho[i1]
    caminho[i1] = caminho[i2]
    caminho[i2] = temp
    return caminho

def get_melhor_variacao(caminho, m):
    melhor_caminho = caminho
    melhor_custo = calc_custo(caminho, m)
    count = 0
    for i in range(1, len(caminho)-2):
        for j in range(i+1, len(caminho)-1):
            count += 1
            path = caminho.copy()
            novo = swap(path, i, j)
            custo = calc_custo(novo, m)
            if custo < melhor_custo:
                melhor_custo = custo
                melhor_caminho = novo
    return melhor_caminho

def trocar_pares(caminho, m):
    solutions = []
    for i in range(1, len(caminho)-2):
        for j in range(i+1, len(caminho)-1):
            path = caminho.copy()
            novo = swap(path, i, j)
            solutions.append(novo)
    return solutions

def otimizar(caminho, m):
    best_caminho = caminho
    best_custo = calc_custo(best_caminho, m)
    pares = trocar_pares(caminho, m)
    testes = pow(len(pares), 2)
    for par in pares:
        melhor_par = get_melhor_variacao(par, m)
        custo = calc_custo(melhor_par, m)
        if custo < best_custo:
            print('Um caminho melhor de custo {} foi encontrado!'.format(custo))
            best_caminho = melhor_par
            best_custo = custo
    print('\nOtimização finalizada. {} soluções foram testadas'.format(testes))
    return best_caminho

print('Carregando matriz\n')
inicio = time()
M = carregarMatriz()
fim = time()
tempo_carregar = round(fim - inicio, 2)

#imprimirMatriz(M)

print('Calculando caminho inicial\n')
inicio = time()
C = resolver_guloso(M)
fim = time()
tempo_guloso = round(fim - inicio, 2)

print('Caminho guloso: {}\n'.format(C))
print('Custo inicial: {}\n'.format(calc_custo(C,M)))

print('Otimizando Caminho...\n')
inicio = time()
melhor_caminho = C
melhor_custo = calc_custo(C, M)
C2 = otimizar(C, M)
fim = time()
tempo_otimizacao = round(fim - inicio, 2)

tempo = tempo_carregar + tempo_guloso + tempo_otimizacao
custo = calc_custo(C2, M)
print('\nCaminho final: {}'.format(C2))
print('\nCusto final: {}'.format(custo))

print('\nTempo para carregar a matriz: {} seg'.format(tempo_carregar))
print('Tempo da resolução gulosa: {} seg'.format(tempo_guloso))
print('Tempo para otimizar o caminho: {} seg\n'.format(tempo_otimizacao))
print('Tempo total: {} seg'.format(round(tempo, 2)))