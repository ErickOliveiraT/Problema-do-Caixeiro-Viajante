# Solução Utilizando Programação Linear Inteira
A solução foi implementada em python(v2.7) utilizando a biblioteca **pyomo** para modelar o problema, em conjunto com o resolvedor **cplex** da IBM para encontrar a solução.

## Instalando dependências(pyomo e cplex)
### Pyomo
Utilizando o gerenciador de pacotes **pip** da linguagem python, executar o comando:
```sh
pip install pyomo
```

### IBM CPLEX
Baixar o resolvedor IBM CPLEX([Baixar](https://www.ibm.com/developerworks/br/downloads/ws/ilogcplex/index.html "Aqui"))
Instale utilizando o [Tutorial](https://www.ibm.com/support/knowledgecenter/SSSA5P_12.7.1/ilog.odms.cplex.help/CPLEX/GettingStarted/topics/set_up/Python_setup.html "Tutorial")

**Obs: **A implementação atual utiliza a instalação do cplex atribuindo a variável de ambiente PYTHONPATH para o caminho do CPLEX(como descrito no tutorial oficial), caso não tenha atribuido a variável de ambiente, referencie o caminho do resolvedor no código(tsp_pli.py) como abaixo:
```sh
solver = pyEnv.SolverFactory('cplex', executable="/opt/ibm/ILOG/CPLEX_Studio_Community129/cplex/bin/x86-64_linux/cplex")

```
## Execução

```sh
# navegue até o diretório Problema-do-Caixeiro-Viajante/src/exato/
cd Problema-do-Caixeiro-Viajante/src/exato/
# execute o comando abaixo passando o nome da instancia a ser utilizada
python tsp_pli.py nome_instancia.txt
# exemplo
python tsp_pli.py instance_20_3.txt
```

