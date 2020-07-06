from time import time

#Config:
path = '../../instances/'
instances = [{'file': 'instance_10_1.txt'},{'file': 'instance_10_2.txt'},{'file': 'instance_10_3.txt'},
{'file': 'instance_20_1.txt'},{'file': 'instance_20_2.txt'},{'file': 'instance_20_3.txt'},
{'file': 'instance_30_1.txt'},{'file': 'instance_30_2.txt'},{'file': 'instance_30_3.txt'},
{'file': 'instance_40_1.txt'},{'file': 'instance_40_2.txt'},{'file': 'instance_40_3.txt'},
{'file': 'instance_50_1.txt'},{'file': 'instance_50_2.txt'},{'file': 'instance_50_3.txt'},
{'file': 'instance_60_1.txt'},{'file': 'instance_60_2.txt'},{'file': 'instance_60_3.txt'},
{'file': 'instance_70_1.txt'},{'file': 'instance_70_2.txt'},{'file': 'instance_70_3.txt'},
{'file': 'instance_80_1.txt'},{'file': 'instance_80_2.txt'},{'file': 'instance_80_3.txt'},
{'file': 'instance_90_1.txt'},{'file': 'instance_90_2.txt'},{'file': 'instance_90_3.txt'},
{'file': 'instance_100_1.txt'},{'file': 'instance_100_2.txt'},{'file': 'instance_100_3.txt'}]
results = open('results.txt', 'w')

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
    return [melhor_caminho, melhor_custo]

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
        info = get_melhor_variacao(par, m)
        melhor_par = info[0]
        custo = info[1]
        if custo < best_custo:
            print('Um caminho melhor de custo {} foi encontrado!'.format(custo))
            best_caminho = melhor_par
            best_custo = custo
    print('\nOtimização finalizada. {} soluções foram testadas'.format(testes))
    return best_caminho

inicio_benchmark = time()
for ins in instances:
    print('\nInstância: {}'.format(ins['file']))
    results.write('Instancia: {}\n\n'.format(ins['file']))
    instance = open(path+ins['file'], 'r')
    print('Carregando matriz\n')
    inicio = time()
    M = carregarMatriz()
    fim = time()
    tempo_carregar = round(fim - inicio, 2)

    print('Calculando caminho inicial\n')
    inicio = time()
    C = resolver_guloso(M)
    fim = time()
    tempo_guloso = round(fim - inicio, 2)

    print('Caminho guloso: {}\n'.format(C))
    custo_inicial = calc_custo(C,M)
    print('Custo inicial: {}\n'.format(custo_inicial))
    results.write('Custo inicial: {}\n'.format(custo_inicial))

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
    results.write('Custo final: {}\n'.format(custo))

    print('\nTempo para carregar a matriz: {} seg'.format(tempo_carregar))
    results.write('\nTempo para carregar a matriz: {} seg\n'.format(tempo_carregar))
    print('Tempo da resolução gulosa: {} seg'.format(tempo_guloso))
    results.write('Tempo da resolucao gulosa: {} seg\n'.format(tempo_guloso))
    print('Tempo para otimizar o caminho: {} seg\n'.format(tempo_otimizacao))
    results.write('Tempo para otimizar o caminho: {} seg\n'.format(tempo_otimizacao))
    print('Tempo total: {} seg'.format(round(tempo, 2)))
    results.write('Tempo total: {} seg\n\n'.format(round(tempo, 2)))
fim_benchmark = time()

tempo_benchmark = round(fim_benchmark - inicio_benchmark, 2)
print('\n\nTempo de benchmark: {} s'.format(tempo_benchmark))
results.write('Tempo de benchmark: {} s'.format(tempo_benchmark))
results.close()