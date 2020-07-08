import pyomo.environ as pyEnv
import sys
import time

cost_matrix = []

start_time = time.time()

# Le instancia
file = open('../../instances/' + sys.argv[1])
lines = file.readlines()
file.close()

read_matrix_time = time.time() - start_time

for i in range(1, len(lines)):
    aux = lines[i][:-1].split('\t')
    # change instance characters 0 to 999
    for c in range(len(aux)):
        print(c)
        if aux[c] == '0':
            aux[c] = '999'

    aux = [int(i) for i in aux if i!= '' and i!= '\n']
    cost_matrix.append(aux)


# print(cost_matrix)
# exit()
n = len(cost_matrix)

# Inicializa modelo e parametros

# Cria Modelo
model = pyEnv.ConcreteModel()

# Indices das cidades
model.M = pyEnv.RangeSet(n) # 1..n
model.N = pyEnv.RangeSet(n) # 1..n

# Indice de U(usada para evitar subtours)
model.U = pyEnv.RangeSet(2,n)

# Variavel de decisao xij
model.x = pyEnv.Var(model.N,model.M, within=pyEnv.Binary)

# Variavel ui
model.u = pyEnv.Var(model.N, within=pyEnv.NonNegativeIntegers,bounds=(0,n-1))

# Matrix de Custo cij
model.c = pyEnv.Param(model.N, model.M,initialize=lambda model, i, j: cost_matrix[i-1][j-1])

def obj_func(model):
    return sum(model.x[i,j] * model.c[i,j] for i in model.N for j in model.M)

model.objective = pyEnv.Objective(rule=obj_func,sense=pyEnv.minimize)

##------------------------------------------------------##
# Restricao 1

def rule_const1(model,M):
    return sum(model.x[i,M] for i in model.N if i!=M ) == 1

model.const1 = pyEnv.Constraint(model.M,rule=rule_const1)
##------------------------------------------------------##
# Restricao 2

def rule_const2(model,N):
    return sum(model.x[N,j] for j in model.M if j!=N) == 1

model.rest2 = pyEnv.Constraint(model.N,rule=rule_const2)
##------------------------------------------------------##
# Restricao 3

def rule_const3(model,i,j):
    if i!=j: 
        return model.u[i] - model.u[j] + model.x[i,j] * n <= n-1
    else:
        #Yeah, this else doesn't say anything
        return model.u[i] - model.u[i] == 0 
    
model.rest3 = pyEnv.Constraint(model.U,model.N,rule=rule_const3)


##-------------------------RESOLVENDO MODELO--------------------##
# Mostra modelo
model.pprint()

# Resolve
# solver = pyEnv.SolverFactory('cplex', executable="/opt/ibm/ILOG/CPLEX_Studio_Community129/cplex/bin/x86-64_linux/cplex")
solver = pyEnv.SolverFactory('cplex')
result = solver.solve(model,tee = False)

# Mostra resultados
print(result)
result.write()
##-------------------------Resultado--------------------##

List = list(model.x.keys())
solution = []
for i in List:
    if model.x[i]() != 0:
        print(i,'--', model.x[i]())
        solution.append(i[1])

f = 0
totalCost = 0
solutionPath = [1]
for k in range(len(solution)):
    solutionPath.append(solution[f])
    f = solution[f]-1
    totalCost = totalCost + cost_matrix[f][solution[f]-1]

print('Custo total: ', totalCost)
print('Tempo Leitura Matrix: ', read_matrix_time)
print('Tempo Total: ', time.time() - start_time)
print('Path: ', solutionPath)