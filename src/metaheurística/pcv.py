from time import time
import sys

#Config:
path = '../../instances/' + sys.argv[1]
instance = open(path, 'r') #Instância (pasta src/instances)

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

def calc_custo(caminho, m): #Calcula o custo de um caminho
    custo = 0
    for i in range(0, len(caminho)-1):
        custo += m[caminho[i]][caminho[i+1]]
    return custo

def swap(caminho, i1, i2): #Troca duas cidades de posição em um caminho
    temp = caminho[i1]
    caminho[i1] = caminho[i2]
    caminho[i2] = temp
    return caminho

def get_melhor_variacao(caminho, m): #Dado uma solução plausível, retorna a de melhor custo entre as soluções geradas por trocas 2-opt
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
    return [melhor_caminho, melhor_custo]

def trocar_pares(caminho, m): #Retorna as soluções geradas a partir das trocas 2-opt
    solutions = []
    for i in range(1, len(caminho)-2):
        for j in range(i+1, len(caminho)-1):
            path = caminho.copy()
            novo = swap(path, i, j)
            solutions.append(novo)
    return solutions

def otimizar(caminho, m): #Realiza o processo de otimização
    best_caminho = caminho
    best_custo = calc_custo(best_caminho, m)
    pares = trocar_pares(caminho, m)
    testes = pow(len(pares), 2)
    for par in pares:
        info = get_melhor_variacao(par, m)
        melhor_par = info[0]
        custo = info[1]
        if custo < best_custo:
            print('Um caminho melhor de custo {} foi encontrado!'.format(custo))
            best_caminho = melhor_par
            best_custo = custo
    print('\nOtimização finalizada. {} soluções foram testadas'.format(testes))
    return best_caminho

print('Instância: {}\n'.format(path))
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
custo_inicial = calc_custo(C,M)
print('Custo inicial: {}\n'.format(custo_inicial))

print('Otimizando Caminho...\n')
inicio = time()
melhor_caminho = C
melhor_custo = custo_inicial
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